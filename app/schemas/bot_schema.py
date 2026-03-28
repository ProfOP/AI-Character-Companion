from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BotCreate(BaseModel):
    name: str
    description: Optional[str] = None
    system_prompt: str
    initial_message: Optional[str] = None
    is_public: bool = True


class BotUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    system_prompt: Optional[str] = None
    initial_message: Optional[str] = None
    is_public: Optional[bool] = None


class BotResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    system_prompt: str
    initial_message: Optional[str]
    is_public: bool
    created_at: datetime