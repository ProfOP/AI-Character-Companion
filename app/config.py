import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not set")

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL not set")

    if not SECRET_KEY:
        raise ValueError("SECRET_KEY not set")


settings = Settings()