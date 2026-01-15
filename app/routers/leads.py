import json
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Lead, AuditLog
from app.schemas import ContactLeadIn, QuoteLeadIn, PlannerLeadIn, AuditRequestIn
from app.rate_limit import rate_limit
from app.emailer import send_email

router = APIRouter()

def _create_lead(db: Session, kind: str, full_name: str, email: str, subject: str | None, payload_obj: dict):
    lead = Lead(
        kind=kind,
        full_name=full_name,
        email=email,
        subject=subject,
        payload=json.dumps(payload_obj, ensure_ascii=False),
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)

    db.add(AuditLog(actor="system", action="create", entity="lead", entity_id=lead.id, detail=kind))
    db.commit()
    return lead

@router.post("/api/leads/contact")
def create_contact_lead(body: ContactLeadIn, request: Request, db: Session = Depends(get_db)):
    rate_limit(request, "leads_contact", limit=10, window_seconds=60)
    lead = _create_lead(db, "contact", body.full_name, body.email, body.subject, body.model_dump())

    send_email(
        to="bluewavedigital.business@gmail.com",
        subject=f"[BlueWave] Contact Lead: {body.subject}",
        body=f"Name: {body.full_name}\nEmail: {body.email}\n\nMessage:\n{body.message}",
    )
    return {"ok": True, "id": lead.id}

@router.post("/api/leads/quote")
def create_quote_lead(body: QuoteLeadIn, request: Request, db: Session = Depends(get_db)):
    rate_limit(request, "leads_quote", limit=10, window_seconds=60)
    lead = _create_lead(db, "quote", body.full_name, body.email, f"Quote: {body.service}", body.model_dump())

    send_email(
        to="bluewavedigital.business@gmail.com",
        subject=f"[BlueWave] Quote Request: {body.service}",
        body=f"Name: {body.full_name}\nEmail: {body.email}\nService: {body.service}\nBudget: {body.budget_range}\n\nDetails:\n{body.details}",
    )
    return {"ok": True, "id": lead.id}

@router.post("/api/leads/planner")
def create_planner_lead(body: PlannerLeadIn, request: Request, db: Session = Depends(get_db)):
    rate_limit(request, "leads_planner", limit=10, window_seconds=60)
    lead = _create_lead(db, "planner", body.full_name, body.email, f"Planner: {body.project_type}", body.model_dump())
    return {"ok": True, "id": lead.id}

@router.post("/api/leads/audit")
def create_audit_request(body: AuditRequestIn, request: Request, db: Session = Depends(get_db)):
    rate_limit(request, "leads_audit", limit=6, window_seconds=60)
    lead = _create_lead(db, "audit", body.full_name, body.email, "Website audit request", body.model_dump())
    return {"ok": True, "id": lead.id}
