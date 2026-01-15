from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.security import require_admin
from app.models import Lead, Application, Job
from app.schemas import AdminLeadRow, AdminApplicationRow

router = APIRouter()

@router.get("/api/admin/leads", response_model=list[AdminLeadRow])
def admin_list_leads(_: str = Depends(require_admin), db: Session = Depends(get_db)):
    rows = db.query(Lead).order_by(Lead.created_at.desc()).limit(200).all()
    out = []
    for r in rows:
        out.append(AdminLeadRow(
            id=r.id, kind=r.kind, full_name=r.full_name, email=r.email,
            subject=r.subject, created_at=r.created_at
        ))
    return out

@router.get("/api/admin/applications", response_model=list[AdminApplicationRow])
def admin_list_applications(_: str = Depends(require_admin), db: Session = Depends(get_db)):
    rows = db.query(Application).order_by(Application.created_at.desc()).limit(200).all()
    out = []
    for r in rows:
        job = db.query(Job).filter(Job.id == r.job_id).first()
        out.append(AdminApplicationRow(
            id=r.id, job_slug=(job.slug if job else "unknown"),
            full_name=r.full_name, email=r.email, status=r.status,
            created_at=r.created_at
        ))
    return out
