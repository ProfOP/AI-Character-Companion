from pydantic import BaseModel
from typing import Optional


class StyleConfig(BaseModel):
    tone: Optional[str] = None
    intensity: Optional[int] = None
    style: Optional[str] = None


class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    bot_id: str
    message: str
    style_config: Optional[StyleConfig] = None


class ChatResponse(BaseModel):
    reply: str
    conversation_id: str