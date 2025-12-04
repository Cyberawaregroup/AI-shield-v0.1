from datetime import datetime, timezone
import json
import logging
from typing import List
import uuid

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db import get_session
from app.db.chatbot import ChatMessage, ChatSession, FraudReport
from app.api.v1.schemas.chatbot import (
    ChatMessageCreate,
    ChatMessageResponse,
    ChatSessionCreate,
    ChatSessionResponse,
    FraudReportCreate,
    FraudReportResponse,
)
from app.services.chatbot import ChatbotService
from app.services.huggingface import HuggingFaceService

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


def generate_session_id():
    """Generate a unique session ID"""
    return str(uuid.uuid4())


@router.post("/sessions", response_model=ChatSessionResponse)
async def create_chat_session(
    session_data: ChatSessionCreate,
    db_session: Session = Depends(get_session),
    chatbot_service: ChatbotService = Depends(get_chatbot_service),
):
    """
    Create a new chat session for fraud advice (No auth required)
    """
    try:
        # Create chat session with default user ID
        chat_session = ChatSession(
            user_id=1,  # Default user ID for demo
            session_id=generate_session_id(),
            fraud_type=session_data.fraud_type,
            vulnerability_factors_list=session_data.vulnerability_factors or [],
        )

        db_session.add(chat_session)
        db_session.commit()
        db_session.refresh(chat_session)

        return ChatSessionResponse(
            id=chat_session.id,
            session_id=chat_session.session_id,
            user_id=chat_session.user_id,
            fraud_type=chat_session.fraud_type,
            status=chat_session.status,
            vulnerability_factors=chat_session.vulnerability_factors_list,
            created_at=chat_session.created_at.isoformat(),
            updated_at=chat_session.updated_at.isoformat(),
            last_activity=chat_session.last_activity.isoformat(),
        )
    except Exception as e:
        logger.error(f"Error creating chat session: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create chat session")


@router.get("/sessions", response_model=List[ChatSessionResponse])
async def get_user_sessions(
    db_session: Session = Depends(get_session), skip: int = 0, limit: int = 100
):
    """
    Get all chat sessions (No auth required - demo only)
    """
    try:
        sessions = (
            db_session.execute(
                select(ChatSession)
                .where(ChatSession.user_id == 1)  # Default user ID
                .order_by(ChatSession.created_at.desc())
                .offset(skip)
                .limit(limit)
            )
            .scalars()
            .all()
        )

        return [
            ChatSessionResponse(
                id=session.id,
                session_id=session.session_id,
                user_id=session.user_id,
                fraud_type=session.fraud_type,
                status=session.status,
                vulnerability_factors=session.vulnerability_factors_list,
                created_at=session.created_at.isoformat(),
                updated_at=session.updated_at.isoformat(),
                last_activity=session.last_activity.isoformat(),
            )
            for session in sessions
        ]
    except Exception as e:
        logger.error(f"Error fetching chat sessions: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch chat sessions")


@router.get("/sessions/{session_id}/messages", response_model=List[ChatMessageResponse])
async def get_chat_messages(
    session_id: str,
    db_session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
):
    """
    Get chat messages for a session (No auth required)
    """
    try:
        # Find session by session_id
        session = db_session.execute(
            select(ChatSession).where(ChatSession.session_id == session_id)
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

        return [
            ChatMessageResponse(
                id=msg.id,
                session_id=msg.session_id,
                message_type=msg.message_type,
                content=msg.content,
                metadata=msg.message_metadata or {},
                ai_model=msg.ai_model,
                ai_confidence=msg.ai_confidence,
                ai_reasoning=msg.ai_reasoning,
                created_at=msg.created_at.isoformat(),
            )
            for msg in messages
        ]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching chat messages: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch chat messages")


@router.post("/sessions/{session_id}/messages", response_model=ChatMessageResponse)
async def send_message(
    session_id: str,
    message: ChatMessageCreate,
    db_session: Session = Depends(get_session),
    chatbot_service: ChatbotService = Depends(get_chatbot_service),
    huggingface_service: HuggingFaceService = Depends(get_huggingface_service),
):
    """
    Send a message in a chat session and get AI response (No auth required)
    """
    try:
        # Find session by session_id
        session = db_session.execute(
            select(ChatSession).where(ChatSession.session_id == session_id)
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
            metadata=message.metadata or {},
        )
        db_session.add(user_message)
        db_session.commit()

        # Generate AI response
        session_context = {
            "fraud_type": session.fraud_type,
            "vulnerability_factors": session.vulnerability_factors_list,
        }

        ai_response = await chatbot_service.generate_response(
            user_message=message.content,
            session_context=session_context,
            user_id=session.user_id,
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
        db_session.commit()

        return ChatMessageResponse(
            id=bot_message.id,
            session_id=bot_message.session_id,
            message_type=bot_message.message_type,
            content=bot_message.content,
            metadata=bot_message.message_metadata or {},
            ai_model=bot_message.ai_model,
            ai_confidence=bot_message.ai_confidence,
            ai_reasoning=bot_message.ai_reasoning,
            created_at=bot_message.created_at.isoformat(),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to send message")


@router.post("/fraud-reports", response_model=FraudReportResponse)
async def create_fraud_report(
    report_data: FraudReportCreate, db_session: Session = Depends(get_session)
):
    """
    Create a fraud report (No auth required)
    """
    try:
        fraud_report = FraudReport(
            user_id=1,  # Default user ID
            fraud_type=report_data.fraud_type,
            description=report_data.description,
            amount_lost=report_data.amount_lost,
            contact_info=report_data.contact_info,
            evidence_links_list=report_data.evidence_links or [],
            status="pending",
        )

        db_session.add(fraud_report)
        db_session.commit()
        db_session.refresh(fraud_report)

        return FraudReportResponse.from_orm(fraud_report)
    except Exception as e:
        logger.error(f"Error creating fraud report: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create fraud report")


@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for real-time chat (No auth required)
    """
    await websocket.accept()

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)

            # Process message and generate response
            # This would integrate with the chatbot service
            response = {
                "type": "bot_message",
                "content": f"AI Response to: {message_data.get('content', '')}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

            # Send response back to client
            await websocket.send_text(json.dumps(response))

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for session {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        await websocket.close()
