from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = Field(alias="DATABASE_URL")

    jwt_secret: str = Field(alias="JWT_SECRET")
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 60 * 24  # 24 hours

    allowed_origins: str = Field(default="*", alias="ALLOWED_ORIGINS")

    admin_email: str = Field(default="admin@bluewavedigital.com", alias="ADMIN_EMAIL")
    admin_password: str = Field(default="ChangeThis123!", alias="ADMIN_PASSWORD")

    upload_dir: str = "storage/uploads"
    max_upload_mb: int = 15  # keep conservative; can increase later

settings = Settings()
