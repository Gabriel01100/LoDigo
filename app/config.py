from pydantic_settings  import BaseSettings, SettingsConfigDict
from typing import List

COOKIE_NAME = "anon_key"

###CORS#####
class Settings(BaseSettings):


    model_config = SettingsConfigDict(
        env_file=".env",          # Lee variables del archivo .env
        env_file_encoding="utf-8"
    )
    CORS_ORIGINS:List[str] = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:5173",  # Vite
    "http://127.0.0.1:5173",
    ]
    # JWT / Seguridad
    SECRET_KEY: str = "default_secret"

    # Environment
    ENVIRONMENT: str = "development"

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    DB_ECHO:bool=False

    HCAPTCHA_SITE_KEY: str | None = None
    HCAPTCHA_SECRET_KEY: str | None = None




settings = Settings()