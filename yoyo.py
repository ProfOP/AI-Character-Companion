from sqlalchemy import create_engine
import os

DATABASE_URL = "postgresql://postgres:border@localhost:5432/ai_clone"

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        print("Connected successfully!")
except Exception as e:
    print("Connection failed:", e)
