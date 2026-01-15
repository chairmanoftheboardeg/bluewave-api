from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Job
from app.schemas import JobOut, JobDetailOut

router = APIRouter()

@router.get("/api/jobs", response_model=list[JobOut])
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).filter(Job.is_active == True).order_by(Job.created_at.desc()).all()
    return jobs

@router.get("/api/jobs/{slug}", response_model=JobDetailOut)
def get_job(slug: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.slug == slug, Job.is_active == True).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
