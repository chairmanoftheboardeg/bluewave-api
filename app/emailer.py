import httpx
from app.settings import settings

RESEND_API = "https://api.resend.com/emails"

async def send_email(subject: str, html: str) -> None:
    headers = {
        "Authorization": f"Bearer {settings.RESEND_API_KEY}",
        "Content-Type": "application/json",
    }

    from_email = "onboarding@resend.dev"

    payload = {
        "from": from_email,
        "to": [settings.NOTIFY_EMAIL_TO],
        "subject": subject,
        "html": html,
    }

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(RESEND_API, headers=headers, json=payload)
        r.raise_for_status()
