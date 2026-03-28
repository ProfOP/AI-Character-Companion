import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Conversation, Message, Memory, Bot
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.ai_service import generate_response
from app.services.memory_service import update_memory_summary
from app.services.dependencies import get_current_user

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    # 1️⃣ Fetch bot
    bot = db.query(Bot).filter(Bot.id == request.bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")

    if not bot.is_public and bot.creator_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    # 2️⃣ Fetch or create conversation
    if request.conversation_id:
        conversation = db.query(Conversation).filter(
            Conversation.id == request.conversation_id,
            Conversation.user_id == current_user.id
        ).first()
    else:
        conversation = None

    if not conversation:
        conversation = Conversation(
            id=uuid.uuid4(),
            title=bot.name,
            bot_id=bot.id,
            user_id=current_user.id,
            style_config=request.style_config.dict() if request.style_config else None
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        memory = Memory(
            conversation_id=conversation.id,
            summary=""
        )
        db.add(memory)
        db.commit()

        # Initial message
        if bot.initial_message:
            initial_msg = Message(
                conversation_id=conversation.id,
                role="assistant",
                content=bot.initial_message
            )
            db.add(initial_msg)
            db.commit()

            updated_memory = await update_memory_summary(
                previous_summary="",
                conversation=f"ASSISTANT: {bot.initial_message}"
            )
            memory.summary = updated_memory
            db.commit()

    # 🔥 UPDATE STYLE IF USER PROVIDED NEW ONE
    if request.style_config:
        conversation.style_config = request.style_config.dict()
        db.commit()

    # 3️⃣ Save user message
    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=request.message
    )
    db.add(user_message)
    db.commit()

    # 4️⃣ Fetch messages
    messages = db.query(Message).filter(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at).all()

    formatted_messages = [
        {"role": m.role, "content": m.content}
        for m in messages
    ]

    # 5️⃣ Fetch memory
    memory = db.query(Memory).filter(
        Memory.conversation_id == conversation.id
    ).first()

    # 🔥 USE STORED STYLE
    style_config = conversation.style_config

    # 6️⃣ Generate reply
    reply = await generate_response(
        character_prompt=bot.system_prompt,
        messages=formatted_messages,
        memory_summary=memory.summary if memory else "",
        style_config=style_config
    )

    # 7️⃣ Save assistant message
    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=reply
    )
    db.add(assistant_message)
    db.commit()

    # 8️⃣ Update memory
    updated_messages = formatted_messages + [{"role": "assistant", "content": reply}]

    conversation_text = "\n".join(
        [f"{msg['role'].upper()}: {msg['content']}" for msg in updated_messages]
    )

    updated_memory = await update_memory_summary(
        previous_summary=memory.summary if memory else "",
        conversation=conversation_text,
    )

    memory.summary = updated_memory
    db.commit()

    return ChatResponse(
        reply=reply,
        conversation_id=str(conversation.id)
    )