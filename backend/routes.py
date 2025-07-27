from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

from model import User, SessionLocal

SECRET_KEY = "your-secret-key"  # Change this in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/signup", response_model=Token)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token = create_access_token(data={"sub": new_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"} 


from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
import aiofiles
from pathlib import Path
# import magic
from datetime import datetime

from scam_models import ScamReport, ScamEvidence, User
from scam_schemas import (
    ScamReportCreate, 
    ScamReportResponse, 
    ScamReportSummary,
    ScamReportStats,
    EvidenceFileResponse
)
from model import SessionLocal  # Assuming this exists from your existing code

router = APIRouter()
security = HTTPBearer(auto_error=False)

# Configuration
UPLOAD_DIR = Path("uploads/evidence")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx', '.txt'}
ALLOWED_MIME_TYPES = {
    'image/jpeg', 'image/png', 'image/gif', 'image/webp',
    'application/pdf', 'application/msword', 
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain'
}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: Optional[str] = Depends(security), db: Session = Depends(get_db)):
    """Get current user if authenticated, otherwise return None for anonymous reporting"""
    if not token:
        return None

    # Add your JWT token validation logic here
    # This is a simplified version - implement proper JWT validation
    try:
        # Decode JWT and get user_id
        # user_id = decode_jwt_token(token.credentials)
        # user = db.query(User).filter(User.id == user_id).first()
        # return user
        return None  # Placeholder for now
    except:
        return None

def validate_file(file: UploadFile) -> dict:
    """Validate uploaded file"""
    errors = []

    # Check file size
    if file.size and file.size > MAX_FILE_SIZE:
        errors.append(f"File size ({file.size} bytes) exceeds maximum allowed size ({MAX_FILE_SIZE} bytes)")

    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        errors.append(f"File extension '{file_ext}' is not allowed. Allowed extensions: {', '.join(ALLOWED_EXTENSIONS)}")

    # Check MIME type (would need python-magic library)
    # if file.content_type not in ALLOWED_MIME_TYPES:
    #     errors.append(f"File type '{file.content_type}' is not allowed")

    return {"valid": len(errors) == 0, "errors": errors}

async def save_file(file: UploadFile, scam_report_id: int, db: Session) -> ScamEvidence:
    """Save uploaded file and create database record"""
    # Generate unique filename
    file_ext = Path(file.filename).suffix.lower()
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename

    # Save file to disk
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)

    # Create database record
    evidence = ScamEvidence(
        scam_report_id=scam_report_id,
        filename=unique_filename,
        original_filename=file.filename,
        file_path=str(file_path),
        file_size=len(content),
        file_type=file.content_type or 'application/octet-stream'
    )

    db.add(evidence)
    db.commit()
    db.refresh(evidence)

    return evidence

@router.post("/reports", response_model=ScamReportResponse, status_code=status.HTTP_201_CREATED)
async def create_scam_report(
    # Form data
    reporter_name: Optional[str] = Form(None),
    reporter_email: Optional[str] = Form(None),
    reporter_phone: Optional[str] = Form(None),
    incident_date: str = Form(...),
    incident_time: Optional[str] = Form(None),
    scam_type: str = Form(...),
    other_scam_type: Optional[str] = Form(None),
    description: str = Form(...),
    how_scam_began: Optional[str] = Form(None),
    money_lost: bool = Form(False),
    amount_lost: Optional[float] = Form(None),
    payment_method: Optional[str] = Form(None),
    scammer_email: Optional[str] = Form(None),
    scammer_phone: Optional[str] = Form(None),
    scammer_website: Optional[str] = Form(None),
    scammer_social_media: Optional[str] = Form(None),
    is_reporter_victim: bool = Form(True),
    victim_relation: Optional[str] = Form(None),
    victim_age_group: Optional[str] = Form(None),
    information_accurate: bool = Form(...),
    consent_to_contact: bool = Form(False),
    # File uploads
    evidence_files: List[UploadFile] = File(default=[]),
    # Dependencies
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new scam report with optional file evidence"""

    try:
        # Convert form data to Pydantic model for validation
        from datetime import datetime
        report_data = {
            "reporter_name": reporter_name,
            "reporter_email": reporter_email,
            "reporter_phone": reporter_phone,
            "incident_date": datetime.fromisoformat(incident_date).date(),
            "incident_time": incident_time,
            "scam_type": scam_type,
            "other_scam_type": other_scam_type,
            "description": description,
            "how_scam_began": how_scam_began,
            "money_lost": money_lost,
            "amount_lost": amount_lost,
            "payment_method": payment_method,
            "scammer_email": scammer_email,
            "scammer_phone": scammer_phone,
            "scammer_website": scammer_website,
            "scammer_social_media": scammer_social_media,
            "is_reporter_victim": is_reporter_victim,
            "victim_relation": victim_relation,
            "victim_age_group": victim_age_group,
            "information_accurate": information_accurate,
            "consent_to_contact": consent_to_contact
        }

        # Validate using Pydantic model
        validated_data = ScamReportCreate(**report_data)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")

    # Validate evidence files
    file_errors = []
    for i, file in enumerate(evidence_files):
        if file.filename:  # Skip empty file inputs
            validation = validate_file(file)
            if not validation["valid"]:
                file_errors.extend([f"File {i+1}: {error}" for error in validation["errors"]])

    if file_errors:
        raise HTTPException(status_code=400, detail={"file_errors": file_errors})

    # Create scam report
    db_report = ScamReport(
        user_id=current_user.id if current_user else None,
        **validated_data.dict()
    )

    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    # Save evidence files
    evidence_records = []
    for file in evidence_files:
        if file.filename:  # Skip empty file inputs
            try:
                evidence = await save_file(file, db_report.id, db)
                evidence_records.append(evidence)
            except Exception as e:
                # If file saving fails, we should clean up and return error
                db.delete(db_report)
                db.commit()
                raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

    # Refresh to get the evidence files
    db.refresh(db_report)

    return db_report

@router.get("/reports", response_model=List[ScamReportSummary])
def get_scam_reports(
    skip: int = 0,
    limit: int = 100,
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of scam reports (admin only or user's own reports)"""

    query = db.query(ScamReport)

    # If user is not admin, only show their own reports
    if current_user:
        # Add admin check logic here
        # if not current_user.is_admin:
        query = query.filter(ScamReport.user_id == current_user.id)
    else:
        # Anonymous users can't view reports
        raise HTTPException(status_code=401, detail="Authentication required")

    reports = query.offset(skip).limit(limit).all()
    return reports

@router.get("/reports/{report_id}", response_model=ScamReportResponse)
def get_scam_report(
    report_id: int,
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific scam report details"""

    report = db.query(ScamReport).filter(ScamReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    # Check permissions
    if current_user:
        # Add admin check or ownership check
        if report.user_id and report.user_id != current_user.id:
            # Add admin check here
            # if not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Access denied")
    else:
        raise HTTPException(status_code=401, detail="Authentication required")

    return report

@router.get("/reports/{report_id}/evidence/{evidence_id}")
async def download_evidence(
    report_id: int,
    evidence_id: int,
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Download evidence file"""

    # Get the evidence record
    evidence = db.query(ScamEvidence).filter(
        ScamEvidence.id == evidence_id,
        ScamEvidence.scam_report_id == report_id
    ).first()

    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence file not found")

    # Check permissions (similar to get_scam_report)
    report = evidence.scam_report
    if current_user:
        if report.user_id and report.user_id != current_user.id:
            # Add admin check here
            raise HTTPException(status_code=403, detail="Access denied")
    else:
        raise HTTPException(status_code=401, detail="Authentication required")

    # Check if file exists
    file_path = Path(evidence.file_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found on disk")

    from fastapi.responses import FileResponse
    return FileResponse(
        path=file_path,
        filename=evidence.original_filename,
        media_type=evidence.file_type
    )

@router.get("/stats", response_model=ScamReportStats)
def get_scam_stats(
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get scam reporting statistics (admin only)"""

    # Add admin check
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    # Add admin role check here
    # if not current_user.is_admin:
    #     raise HTTPException(status_code=403, detail="Admin access required")

    from sqlalchemy import func

    # Total reports
    total_reports = db.query(ScamReport).count()

    # Reports with financial loss
    reports_with_loss = db.query(ScamReport).filter(ScamReport.money_lost == True).count()

    # Total amount lost
    total_lost = db.query(func.sum(ScamReport.amount_lost)).filter(
        ScamReport.money_lost == True
    ).scalar() or 0.0

    # Most common scam types
    scam_type_counts = db.query(
        ScamReport.scam_type,
        func.count(ScamReport.id).label('count')
    ).group_by(ScamReport.scam_type).order_by(func.count(ScamReport.id).desc()).all()

    most_common_types = [
        {"scam_type": str(row.scam_type), "count": row.count}
        for row in scam_type_counts
    ]

    # Reports by status
    status_counts = db.query(
        ScamReport.status,
        func.count(ScamReport.id).label('count')
    ).group_by(ScamReport.status).all()

    reports_by_status = {row.status: row.count for row in status_counts}

    return ScamReportStats(
        total_reports=total_reports,
        reports_with_financial_loss=reports_with_loss,
        total_amount_lost=total_lost,
        most_common_scam_types=most_common_types,
        reports_by_status=reports_by_status
    )

@router.put("/reports/{report_id}/status")
def update_report_status(
    report_id: int,
    status: str = Form(...),
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update report status (admin only)"""

    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    # Add admin check here
    # if not current_user.is_admin:
    #     raise HTTPException(status_code=403, detail="Admin access required")

    report = db.query(ScamReport).filter(ScamReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    valid_statuses = ["pending", "investigating", "resolved", "dismissed"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")

    report.status = status
    db.commit()

    return {"message": "Status updated successfully", "status": status}
