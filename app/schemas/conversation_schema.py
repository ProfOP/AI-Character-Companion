from pydantic import BaseModel
from datetime import datetime
from typing import List


class ConversationItem(BaseModel):
    id: str
    title: str | None
    created_at: datetime | None
    updated_at: datetime | None


class ConversationListResponse(BaseModel):
    conversations: List[ConversationItem]
