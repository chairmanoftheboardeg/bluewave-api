from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str

    RESEND_API_KEY: str
    NOTIFY_EMAIL_TO: str = "bluewavedigital.business@gmail.com"

    # Comma-separated origins, e.g.:
    # "https://username.github.io,https://example.com"
    CORS_ORIGINS: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

