from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Conversation, Message, Memory
from app.schemas.regenerate_schema import RegenerateRequest, RegenerateResponse
from app.services.regeneration_service import regenerate_response
from app.services.memory_service import update_memory_summary

router = APIRouter()


@router.post("/regenerate", response_model=RegenerateResponse)
async def regenerate(request: RegenerateRequest, db: Session = Depends(get_db)):

    # 1️⃣ Fetch conversation
    conversation = db.query(Conversation).filter(
        Conversation.id == request.conversation_id
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # 2️⃣ Fetch all messages
    messages = db.query(Message).filter(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at).all()

    if not messages:
        raise HTTPException(status_code=400, detail="No messages to regenerate")

    # 3️⃣ Find last assistant message
    last_assistant = None
    for msg in reversed(messages):
        if msg.role == "assistant":
            last_assistant = msg
            break

    if not last_assistant:
        raise HTTPException(status_code=400, detail="No assistant message found")

    last_assistant_content = last_assistant.content

    # 4️⃣ Remove old assistant reply
    db.delete(last_assistant)
    db.commit()

    # 5️⃣ Re-fetch updated message list
    updated_messages = db.query(Message).filter(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at).all()

    formatted_messages = [
        {"role": m.role, "content": m.content}
        for m in updated_messages
    ]

    # 6️⃣ Fetch memory
    memory = db.query(Memory).filter(
        Memory.conversation_id == conversation.id
    ).first()

    # 7️⃣ Generate new reply
    new_reply = await regenerate_response(
        character_prompt=request.character_prompt,
        memory_summary=memory.summary if memory else "",
        conversation="\n".join(
            [f"{msg['role'].upper()}: {msg['content']}" for msg in formatted_messages]
        ),
        last_assistant_reply=last_assistant_content,
        tone_instruction=request.tone_instruction or "",
    )

    # 8️⃣ Save regenerated reply
    regenerated_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=new_reply
    )

    db.add(regenerated_message)
    db.commit()

    # 9️⃣ Recalculate memory from canonical DB state
    final_messages = db.query(Message).filter(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at).all()

    conversation_text = "\n".join(
        [f"{m.role.upper()}: {m.content}" for m in final_messages]
    )

    updated_memory = await update_memory_summary(
        previous_summary="",
        conversation=conversation_text,
    )

    if memory:
        memory.summary = updated_memory
    else:
        memory = Memory(
            conversation_id=conversation.id,
            summary=updated_memory
        )
        db.add(memory)

    db.commit()

    return RegenerateResponse(reply=new_reply)
