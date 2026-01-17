from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str
    RESEND_API_KEY: str
    NOTIFY_EMAIL_TO: str = "bluewavedigital.business@gmail.com"
    CORS_ORIGINS: str = ""

    class Config:
        extra = "ignore"

settings = Settings()
