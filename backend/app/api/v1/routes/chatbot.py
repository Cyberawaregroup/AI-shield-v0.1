from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.db import get_session
from app.db.chatbot import ChatSession, ChatMessage
from app.api.v1.schemas.chatbot import (
    ChatSessionCreate,
    ChatSessionResponse,
    ChatMessageCreate,
    ChatMessageResponse,
)
from app.services.chatbot_service import ChatbotService
from app.services.huggingface_service import HuggingFaceService
from app.core.security import get_user
import logging
import json
from datetime import datetime, timezone

logger = logging.getLogger(__name__)
router = APIRouter()


# Service dependencies
def get_huggingface_service():
    return HuggingFaceService()


def get_threat_intelligence_service():
    from app.services.threat_intelligence import ThreatIntelligenceService

    return ThreatIntelligenceService()


def get_chatbot_service():
    return ChatbotService(
        huggingface_service=get_huggingface_service(),
        threat_service=get_threat_intelligence_service(),
    )


@router.post("/sessions", response_model=ChatSessionResponse)
async def create_chat_session(
    session_data: ChatSessionCreate,
    db_session: Session = Depends(get_session),
    chatbot_service: ChatbotService = Depends(get_chatbot_service),
):
    """
    Create a new chat session for fraud advice
    """
    try:
        # Create chat session
        chat_session = ChatSession(
            user_id=current_user.id,
            session_id=chatbot_service.generate_session_id(),
            fraud_type=session_data.fraud_type,
            initial_message=session_data.initial_message,
            vulnerability_factors=session_data.vulnerability_factors,
            is_vulnerable_user=bool(session_data.vulnerability_factors),
        )

        db_session.add(chat_session)
        db_session.commit()
        db_session.refresh(chat_session)

        # Create initial bot message
        initial_bot_message = await chatbot_service.generate_initial_response(
            session_data.initial_message,
            session_data.fraud_type,
            session_data.vulnerability_factors,
        )

        bot_message = ChatMessage(
            session_id=chat_session.id,
            message_type="bot",
            content=initial_bot_message["content"],
            metadata=initial_bot_message.get("metadata", {}),
            ai_model=initial_bot_message.get("ai_model"),
            ai_confidence=initial_bot_message.get("ai_confidence"),
        )

        db_session.add(bot_message)
        db_session.commit()

        return ChatSessionResponse.from_orm(chat_session)
    except Exception as e:
        logger.error(f"Error creating chat session: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create chat session")


@router.get("/sessions", response_model=List[ChatSessionResponse])
async def get_user_sessions(
    current_user=Depends(get_user),
    db_session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
):
    """
    Get all chat sessions for the current user
    """
    try:
        sessions = (
            db_session.execute(
                select(ChatSession)
                .where(ChatSession.user_id == current_user.id)
                .order_by(ChatSession.created_at.desc())
                .offset(skip)
                .limit(limit)
            )
            .scalars()
            .all()
        )

        return [ChatSessionResponse.from_orm(session) for session in sessions]
    except Exception as e:
        logger.error(f"Error fetching user sessions: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch chat sessions")


@router.get("/sessions/{session_id}", response_model=ChatSessionResponse)
async def get_chat_session(
    session_id: str,
    current_user=Depends(get_user),
    db_session: Session = Depends(get_session),
):
    """
    Get a specific chat session
    """
    try:
        session = db_session.execute(
            select(ChatSession)
            .where(ChatSession.session_id == session_id)
            .where(ChatSession.user_id == current_user.id)
        ).scalar_one_or_none()

        if session is None:
            raise HTTPException(status_code=404, detail="Chat session not found")

        return ChatSessionResponse.from_orm(session)
    except Exception as e:
        logger.error(f"Error fetching chat session {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch chat session")


@router.get("/sessions/{session_id}/messages", response_model=List[ChatMessageResponse])
async def get_chat_messages(
    session_id: str,
    current_user=Depends(get_user),
    db_session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
):
    """
    Get messages for a specific chat session
    """
    try:
        # Verify session belongs to user
        session = db_session.execute(
            select(ChatSession)
            .where(ChatSession.session_id == session_id)
            .where(ChatSession.user_id == current_user.id)
        ).scalar_one_or_none()

        if session is None:
            raise HTTPException(status_code=404, detail="Chat session not found")

        messages = (
            db_session.execute(
                select(ChatMessage)
                .where(ChatMessage.session_id == session.id)
                .order_by(ChatMessage.created_at.asc())
                .offset(skip)
                .limit(limit)
            )
            .scalars()
            .all()
        )

        return [ChatMessageResponse.from_orm(message) for message in messages]
    except Exception as e:
        logger.error(f"Error fetching messages for session {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch chat messages")


@router.post("/sessions/{session_id}/messages", response_model=ChatMessageResponse)
async def send_message(
    session_id: str,
    message: ChatMessageCreate,
    current_user=Depends(get_user),
    db_session: Session = Depends(get_session),
    chatbot_service: ChatbotService = Depends(get_chatbot_service),
    huggingface_service: HuggingFaceService = Depends(get_huggingface_service),
):
    """
    Send a message in a chat session and get AI response
    """
    try:
        # Verify session belongs to user
        session = db_session.execute(
            select(ChatSession)
            .where(ChatSession.session_id == session_id)
            .where(ChatSession.user_id == current_user.id)
        ).scalar_one_or_none()

        if session is None:
            raise HTTPException(status_code=404, detail="Chat session not found")

        if session.status == "closed":
            raise HTTPException(status_code=400, detail="Chat session is closed")

        # Store user message
        user_message = ChatMessage(
            session_id=session.id,
            message_type="user",
            content=message.content,
            metadata=message.metadata,
        )
        db_session.add(user_message)
        db_session.commit()

        # Generate AI response
        ai_response = await chatbot_service.generate_response(
            session_id=session.id, user_message=message.content, session_context=session
        )

        # Store AI response
        bot_message = ChatMessage(
            session_id=session.id,
            message_type="bot",
            content=ai_response["content"],
            metadata=ai_response.get("metadata", {}),
            ai_model=ai_response.get("ai_model"),
            ai_confidence=ai_response.get("ai_confidence"),
            ai_reasoning=ai_response.get("ai_reasoning"),
        )
        db_session.add(bot_message)

        # Update session
        session.last_activity = datetime.now(timezone.utc)
        if ai_response.get("escalate", False):
            session.is_escalated = True
            session.escalation_reason = ai_response.get("escalation_reason")

        db_session.commit()

        return ChatMessageResponse.from_orm(bot_message)
    except Exception as e:
        logger.error(f"Error sending message in session {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to send message")


@router.post("/sessions/{session_id}/escalate")
async def escalate_chat_session(
    session_id: str,
    current_user=Depends(get_user),
    db_session: Session = Depends(get_session),
    chatbot_service: ChatbotService = Depends(get_chatbot_service),
):
    """
    Manually escalate a chat session to human advisor
    """
    try:
        session = db_session.execute(
            select(ChatSession)
            .where(ChatSession.session_id == session_id)
            .where(ChatSession.user_id == current_user.id)
        ).scalar_one_or_none()

        if session is None:
            raise HTTPException(status_code=404, detail="Chat session not found")

        if session.is_escalated:
            raise HTTPException(status_code=400, detail="Session already escalated")

        # Escalate session
        escalation_result = await chatbot_service.escalate_session(session.id)

        session.is_escalated = True
        session.escalated_at = datetime.now(timezone.utc)
        session.escalation_reason = "Manual escalation by user"
        session.status = "escalated"

        db_session.commit()

        return {
            "message": "Session escalated successfully",
            "advisor_id": escalation_result.get("advisor_id"),
        }
    except Exception as e:
        logger.error(f"Error escalating session {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to escalate session")


@router.post("/sessions/{session_id}/close")
async def close_chat_session(
    session_id: str,
    current_user=Depends(get_user),
    db_session: Session = Depends(get_session),
):
    """
    Close a chat session
    """
    try:
        session = db_session.execute(
            select(ChatSession)
            .where(ChatSession.session_id == session_id)
            .where(ChatSession.user_id == current_user.id)
        ).scalar_one_or_none()

        if session is None:
            raise HTTPException(status_code=404, detail="Chat session not found")

        session.status = "closed"
        session.closed_at = datetime.now(timezone.utc)

        db_session.commit()

        return {"message": "Session closed successfully"}
    except Exception as e:
        logger.error(f"Error closing session {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to close session")


@router.post("/sessions/{session_id}/feedback")
async def provide_message_feedback(
    session_id: str,
    message_id: int,
    feedback: str,
    is_helpful: bool,
    current_user=Depends(get_user),
    db_session: Session = Depends(get_session),
):
    """
    Provide feedback on a chatbot message
    """
    try:
        # Verify session belongs to user
        session = db_session.execute(
            select(ChatSession)
            .where(ChatSession.session_id == session_id)
            .where(ChatSession.user_id == current_user.id)
        ).scalar_one_or_none()

        if session is None:
            raise HTTPException(status_code=404, detail="Chat session not found")

        # Update message with feedback
        message = db_session.get(ChatMessage, message_id)
        if message is None or message.session_id != session.id:
            raise HTTPException(status_code=404, detail="Message not found")

        message.user_feedback = feedback
        message.is_helpful = is_helpful

        db_session.commit()

        return {"message": "Feedback recorded successfully"}
    except Exception as e:
        logger.error(f"Error recording feedback: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to record feedback")


# WebSocket endpoint for real-time chat
@router.websocket("/ws/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket, session_id: str, db_session: Session = Depends(get_session)
):
    """
    WebSocket endpoint for real-time chat communication
    """
    await websocket.accept()

    try:
        # Verify session exists
        session = db_session.execute(
            select(ChatSession).where(ChatSession.session_id == session_id)
        ).scalar_one_or_none()

        if session is None:
            await websocket.close(code=4004, reason="Session not found")
            return

        # Send session info
        await websocket.send_text(
            json.dumps(
                {
                    "type": "session_info",
                    "session_id": session_id,
                    "status": session.status,
                }
            )
        )

        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)

            if message_data["type"] == "message":
                # Process message and generate response
                # This would integrate with the chatbot service
                response = {
                    "type": "message",
                    "content": "AI response placeholder",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }

                await websocket.send_text(json.dumps(response))

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for session {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error for session {session_id}: {str(e)}")
        await websocket.close(code=1011, reason="Internal error")
