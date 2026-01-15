from fastapi import APIRouter, HTTPException, status
from app.schemas import AdminLoginIn, TokenOut
from app.config import settings
from app.security import create_access_token

router = APIRouter()

@router.post("/api/auth/login", response_model=TokenOut)
def admin_login(body: AdminLoginIn):
    # Simple admin credential login for MVP.
    # Later: users table + RBAC.
    if body.email.lower() != settings.admin_email.lower() or body.password != settings.admin_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(subject=settings.admin_email)
    return TokenOut(access_token=token)
