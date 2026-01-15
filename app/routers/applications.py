import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Job, Application, AuditLog
from app.config import settings
from app.rate_limit import rate_limit

router = APIRouter()

ALLOWED_CV_EXT = {".pdf", ".doc", ".docx"}

@router.post("/api/applications")
async def submit_application(
    request: Request,
    job_slug: str = Form(...),
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(None),
    cover_letter: str = Form(None),
    cv: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    rate_limit(request, "applications", limit=6, window_seconds=60)

    job = db.query(Job).filter(Job.slug == job_slug, Job.is_active == True).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    cv_filename = None
    cv_path = None

    if cv is not None:
        # size check (best-effort; Content-Length not always present in multipart)
        ext = os.path.splitext(cv.filename or "")[1].lower()
        if ext not in ALLOWED_CV_EXT:
            raise HTTPException(status_code=400, detail="Unsupported CV file type")

        os.makedirs(settings.upload_dir, exist_ok=True)
        safe_name = f"{uuid.uuid4().hex}{ext}"
        path = os.path.join(settings.upload_dir, safe_name)

        contents = await cv.read()
        max_bytes = settings.max_upload_mb * 1024 * 1024
        if len(contents) > max_bytes:
            raise HTTPException(status_code=400, detail=f"File too large (max {settings.max_upload_mb}MB)")

        with open(path, "wb") as f:
            f.write(contents)

        cv_filename = cv.filename
        cv_path = path

    app_row = Application(
        job_id=job.id,
        full_name=full_name,
        email=email,
        phone=phone,
        cover_letter=cover_letter,
        cv_filename=cv_filename,
        cv_path=cv_path,
        status="new",
    )
    db.add(app_row)
    db.commit()
    db.refresh(app_row)

    db.add(AuditLog(actor="system", action="create", entity="application", entity_id=app_row.id, detail=job_slug))
    db.commit()

    return {"ok": True, "id": app_row.id}
