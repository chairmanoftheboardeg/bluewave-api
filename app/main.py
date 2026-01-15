import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers.health import router as health_router
from app.routers.leads import router as leads_router
from app.routers.jobs import router as jobs_router
from app.routers.applications import router as applications_router
from app.routers.auth import router as auth_router
from app.routers.admin import router as admin_router

def _parse_origins(raw: str) -> list[str]:
    raw = (raw or "").strip()
    if raw == "*" or raw == "":
        return ["*"]
    return [o.strip() for o in raw.split(",") if o.strip()]

app = FastAPI(title="BlueWave API", version="1.0.0")

origins = _parse_origins(settings.allowed_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(settings.upload_dir, exist_ok=True)

app.include_router(health_router)
app.include_router(leads_router)
app.include_router(jobs_router)
app.include_router(applications_router)
app.include_router(auth_router)
app.include_router(admin_router)

