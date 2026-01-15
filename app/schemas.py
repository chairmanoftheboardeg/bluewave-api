from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# --- Leads ---
class ContactLeadIn(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    subject: str = Field(min_length=2, max_length=160)
    message: str = Field(min_length=5, max_length=5000)
    company: Optional[str] = Field(default=None, max_length=160)
    phone: Optional[str] = Field(default=None, max_length=40)

class QuoteLeadIn(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    service: str = Field(min_length=2, max_length=120)
    budget_range: Optional[str] = Field(default=None, max_length=80)
    details: str = Field(min_length=5, max_length=5000)
    company: Optional[str] = Field(default=None, max_length=160)
    phone: Optional[str] = Field(default=None, max_length=40)

class PlannerLeadIn(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    project_type: str = Field(min_length=2, max_length=120)
    timeline: Optional[str] = Field(default=None, max_length=80)
    notes: str = Field(min_length=0, max_length=5000)

class AuditRequestIn(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    website_url: str = Field(min_length=5, max_length=300)
    goals: Optional[str] = Field(default=None, max_length=2000)

class LeadOut(BaseModel):
    id: int
    kind: str
    full_name: str
    email: str
    created_at: datetime

# --- Jobs ---
class JobOut(BaseModel):
    id: int
    slug: str
    title: str
    location: str
    department: str
    employment_type: str
    is_active: bool

class JobDetailOut(JobOut):
    description: str

# --- Auth ---
class AdminLoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

# --- Admin lists ---
class AdminLeadRow(BaseModel):
    id: int
    kind: str
    full_name: str
    email: str
    subject: Optional[str] = None
    created_at: datetime

class AdminApplicationRow(BaseModel):
    id: int
    job_slug: str
    full_name: str
    email: str
    status: str
    created_at: datetime
