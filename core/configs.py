from typing import List
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from typing import ClassVar
from sqlalchemy.orm import DeclarativeBase


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI KART-TI"
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpg://postgres:matheus@localhost:5432/kart-ti"
    DBBaseModel: ClassVar[DeclarativeBase] = declarative_base()

    """
    import secrets

    token: str = secrets.token_urlsafe(32)
    """
    JWT_SECRET: str = "p-4bUJXm_uwpi3PnlEAUHu0eB39vhw-CHLQrmhleWSs"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True


settings: Settings = Settings()
