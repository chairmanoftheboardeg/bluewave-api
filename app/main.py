from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from .settings import settings
from .supabase_client import get_supabase
from .schemas import ContactLeadIn, ApplicationIn
from .emailer import send_email
import datetime

app = FastAPI(title="BlueWave API", version="1.0.0")

origins = [o.strip() for o in (settings.CORS_ORIGINS or "").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],  # tighten on Render by setting CORS_ORIGINS
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/jobs")
def list_jobs():
    sb = get_supabase()
    res = sb.table("jobs").select("slug,title,department,location,employment_type,description_html,is_published,created_at").eq("is_published", True).execute()
    return {"jobs": res.data or []}

@app.get("/api/jobs/{slug}")
def get_job(slug: str):
    sb = get_supabase()
    res = sb.table("jobs").select("*").eq("slug", slug).eq("is_published", True).limit(1).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job": res.data[0]}

@app.post("/api/leads/contact")
async def create_contact_lead(payload: ContactLeadIn):
    sb = get_supabase()

    insert_res = sb.table("leads").insert(payload.model_dump()).execute()

    lead_id = None
    if insert_res.data and len(insert_res.data) > 0:
        lead_id = insert_res.data[0].get("id")

    # Email notification (internal)
    safe_msg = (payload.message or "").replace("<", "&lt;").replace(">", "&gt;")
    html = f"""
    <h2>New Contact Lead</h2>
    <p><b>Name:</b> {payload.name}</p>
    <p><b>Email:</b> {payload.email}</p>
    <p><b>Phone:</b> {payload.phone or "-"}</p>
    <p><b>Company:</b> {payload.company or "-"}</p>
    <p><b>Message:</b><br/>{safe_msg}</p>
    <hr/>
    <p><b>UTM Source:</b> {payload.utm_source or "-"}</p>
    <p><b>UTM Medium:</b> {payload.utm_medium or "-"}</p>
    <p><b>UTM Campaign:</b> {payload.utm_campaign or "-"}</p>
    <p><b>Referrer:</b> {payload.referrer or "-"}</p>
    <p><b>Landing Page:</b> {payload.landing_page or "-"}</p>
    <p><b>Lead ID:</b> {lead_id or "-"}</p>
    """

    # Do not fail the API if email fails; but do surface it in logs by raising if you want strict mode.
    try:
        await send_email("BlueWave — New Contact Lead", html)
    except Exception:
        pass

    return {"ok": True, "id": lead_id}

@app.post("/api/applications")
async def create_application(
    # We accept multipart to support optional CV upload
    job_slug: str = Form(...),
    full_name: str = Form(...),
    email: str = Form(...),
    phone: Optional[str] = Form(None),
    portfolio_url: Optional[str] = Form(None),
    cover_letter: Optional[str] = Form(None),
    cv: Optional[UploadFile] = File(None),
):
    sb = get_supabase()

    # Find job by slug
    job_res = sb.table("jobs").select("id,slug,title").eq("slug", job_slug).eq("is_published", True).limit(1).execute()
    if not job_res.data:
        raise HTTPException(status_code=404, detail="Job not found")

    job = job_res.data[0]
    job_id = job["id"]

    app_payload = ApplicationIn(
        job_slug=job_slug,
        full_name=full_name,
        email=email,
        phone=phone,
        portfolio_url=portfolio_url,
        cover_letter=cover_letter
    )

    # Insert application
    insert_app = sb.table("applications").insert({
        "job_id": job_id,
        "full_name": app_payload.full_name,
        "email": str(app_payload.email),
        "phone": app_payload.phone,
        "portfolio_url": str(app_payload.portfolio_url) if app_payload.portfolio_url else None,
        "cover_letter": app_payload.cover_letter,
        "status": "New",
    }).execute()

    if not insert_app.data:
        raise HTTPException(status_code=500, detail="Failed to create application")

    application_id = insert_app.data[0]["id"]

    file_note = ""
    # Optional CV upload to Supabase Storage bucket 'applications'
    if cv is not None:
        allowed = {"application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}
        if cv.content_type not in allowed:
            raise HTTPException(status_code=400, detail="Invalid CV file type (PDF/DOC/DOCX only)")

        content = await cv.read()
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large (max 10MB for MVP)")

        # Path: YYYY/MM/<application_id>/<filename>
        now = datetime.datetime.utcnow()
        storage_path = f"{now.year}/{now.month:02d}/{application_id}/{cv.filename}"

        # Upload
        sb.storage.from_("applications").upload(
            path=storage_path,
            file=content,
            file_options={"content-type": cv.content_type, "upsert": "true"},
        )

        # Store metadata
        sb.table("application_files").insert({
            "application_id": application_id,
            "filename": cv.filename,
            "content_type": cv.content_type,
            "size_bytes": len(content),
            "storage_bucket": "applications",
            "storage_path": storage_path,
        }).execute()

        file_note = f"<p><b>CV uploaded:</b> {storage_path}</p>"

    # Notify internal email
    safe_cover = (cover_letter or "").replace("<", "&lt;").replace(">", "&gt;")
    html = f"""
    <h2>New Job Application</h2>
    <p><b>Job:</b> {job["title"]} ({job["slug"]})</p>
    <p><b>Name:</b> {full_name}</p>
    <p><b>Email:</b> {email}</p>
    <p><b>Phone:</b> {phone or "-"}</p>
    <p><b>Portfolio:</b> {portfolio_url or "-"}</p>
    <p><b>Cover Letter:</b><br/>{safe_cover or "-"}</p>
    <p><b>Application ID:</b> {application_id}</p>
    {file_note}
    """

    try:
        await send_email("BlueWave — New Job Application", html)
    except Exception:
        pass

    return {"ok": True, "id": application_id}
