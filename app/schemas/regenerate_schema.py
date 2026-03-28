from pydantic import BaseModel
from typing import Optional


class RegenerateRequest(BaseModel):
    conversation_id: str
    character_prompt: str
    tone_instruction: Optional[str] = None


class RegenerateResponse(BaseModel):
    reply: str
