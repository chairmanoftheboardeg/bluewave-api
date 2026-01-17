from pydantic import BaseModel, EmailStr, Field, HttpUrl
from typing import Optional

class ContactLeadIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    message: str = Field(min_length=5, max_length=5000)

    phone: Optional[str] = Field(default=None, max_length=50)
    company: Optional[str] = Field(default=None, max_length=120)

    utm_source: Optional[str] = Field(default=None, max_length=200)
    utm_medium: Optional[str] = Field(default=None, max_length=200)
    utm_campaign: Optional[str] = Field(default=None, max_length=200)
    referrer: Optional[str] = Field(default=None, max_length=500)
    landing_page: Optional[str] = Field(default=None, max_length=500)

class ApplicationIn(BaseModel):
    job_slug: str = Field(min_length=2, max_length=200)

    full_name: str = Field(min_length=2, max_length=150)
    email: EmailStr
    phone: Optional[str] = Field(default=None, max_length=50)

    portfolio_url: Optional[HttpUrl] = None
    cover_letter: Optional[str] = Field(default=None, max_length=8000)
