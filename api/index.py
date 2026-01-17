from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from dotenv import load_dotenv
import datetime

load_dotenv()

from app.settings import settings
from app.supabase_client import get_supabase
from app.emailer import send_email

app = FastAPI(title="BlueWave API", version="1.0.0")

origins = [o.strip() for o in (settings.CORS_ORIGINS or "").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
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
    res = sb.table("jobs").select(
        "slug,title,department,location,employment_type,description_html,is_published,created_at"
    ).eq("is_published", True).execute()
    return {"jobs": res.data or []}

@app.get("/api/jobs/{slug}")
def get_job(slug: str):
    sb = get_supabase()
    res = sb.table("jobs").select("*").eq("slug", slug).eq("is_published", True).limit(1).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job": res.data[0]}
