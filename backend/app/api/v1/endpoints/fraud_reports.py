import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.db import get_session
from app.db.chatbot import FraudReport
from app.api.v1.schemas.chatbot import FraudReportCreate

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
async def get_fraud_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_session),
):
    """Get fraud reports"""
    try:
        reports = db.query(FraudReport).offset(skip).limit(limit).all()
        return [
            {
                "id": report.id,
                "fraud_type": report.fraud_type,
                "description": report.description,
                "risk_level": report.risk_level,
                "evidence_files": report.evidence_files_list,
                "evidence_links": report.evidence_links_list,
                "financial_loss": report.financial_loss,
                "status": report.status,
                "reported_at": report.reported_at.isoformat(),
            }
            for report in reports
        ]
    except Exception as e:
        logger.error(f"Error getting fraud reports: {e}")
        return []


@router.post("/")
async def create_fraud_report(
    report_data: FraudReportCreate, db: Session = Depends(get_session)
):
    """Create a new fraud report"""
    try:
        # Create fraud report
        fraud_report = FraudReport(
            fraud_type=report_data.fraud_type,
            description=report_data.description,
            risk_level=report_data.risk_level,
            evidence_files_list=report_data.evidence_files or [],
            evidence_links_list=report_data.evidence_links or [],
            financial_loss=report_data.financial_loss,
        )

        db.add(fraud_report)
        db.commit()
        db.refresh(fraud_report)

        return {
            "id": fraud_report.id,
            "fraud_type": fraud_report.fraud_type,
            "description": fraud_report.description,
            "risk_level": fraud_report.risk_level,
            "message": "Fraud report created successfully",
        }

    except Exception as e:
        logger.error(f"Error creating fraud report: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create fraud report")


@router.get("/{report_id}")
async def get_fraud_report(report_id: int, db: Session = Depends(get_session)):
    """Get fraud report by ID"""
    try:
        report = db.query(FraudReport).filter(FraudReport.id == report_id).first()

        if not report:
            raise HTTPException(status_code=404, detail="Fraud report not found")

        return {
            "id": report.id,
            "fraud_type": report.fraud_type,
            "description": report.description,
            "risk_level": report.risk_level,
            "evidence_files": report.evidence_files_list,
            "evidence_links": report.evidence_links_list,
            "financial_loss": report.financial_loss,
            "status": report.status,
            "reported_at": report.reported_at.isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting fraud report {report_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch fraud report")


@router.put("/{report_id}")
async def update_fraud_report(
    report_id: int, report_update: FraudReportCreate, db: Session = Depends(get_session)
):
    """Update a fraud report"""
    try:
        report = db.query(FraudReport).filter(FraudReport.id == report_id).first()

        if not report:
            raise HTTPException(status_code=404, detail="Fraud report not found")

        # Update fields if provided
        if report_update.fraud_type is not None:
            report.fraud_type = report_update.fraud_type
        if report_update.description is not None:
            report.description = report_update.description
        if report_update.risk_level is not None:
            report.risk_level = report_update.risk_level
        if report_update.evidence_files is not None:
            report.evidence_files_list = report_update.evidence_files
        if report_update.evidence_links is not None:
            report.evidence_links_list = report_update.evidence_links
        if report_update.financial_loss is not None:
            report.financial_loss = report_update.financial_loss

        db.commit()
        db.refresh(report)

        return {
            "id": report.id,
            "fraud_type": report.fraud_type,
            "description": report.description,
            "risk_level": report.risk_level,
            "message": "Fraud report updated successfully",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating fraud report {report_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update fraud report")
