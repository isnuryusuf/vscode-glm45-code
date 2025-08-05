import os
from typing import List

class Settings:
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    
    # CORS
    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:8080").split(",")
    
    # API
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "FastAPI Vue Boilerplate"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    
    class Config:
        case_sensitive = True

settings = Settings()