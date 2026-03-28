from fastapi import FastAPI
from fastapi.security import HTTPBearer
from app.routes.chat import router as chat_router
from app.routes.regenerate import router as regenerate_router
from app.routes.conversations import router as conversations_router
from app.routes.bots import router as bots_router
from app.routes.auth import router as auth_router
from app.database import engine, Base
from app.models import user, conversation, message, memory, bot
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(auth_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(regenerate_router, prefix="/api")
app.include_router(conversations_router, prefix="/api")
app.include_router(bots_router, prefix="/api")
Base.metadata.create_all(bind=engine)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def root():
    return {"message": "Backend is running"}