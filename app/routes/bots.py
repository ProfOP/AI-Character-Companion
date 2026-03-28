import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Bot
from app.schemas.bot_schema import BotCreate, BotUpdate, BotResponse
from app.services.dependencies import get_current_user

router = APIRouter()

UPLOAD_DIR = "uploads/avatars"


# Create Bot
@router.post("/bots", response_model=BotResponse)
def create_bot(
    request: BotCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    bot = Bot(
        name=request.name,
        description=request.description,
        system_prompt=request.system_prompt,
        initial_message=request.initial_message,
        is_public=request.is_public,
        creator_user_id=current_user.id
    )

    db.add(bot)
    db.commit()
    db.refresh(bot)

    return BotResponse(
        id=str(bot.id),
        name=bot.name,
        description=bot.description,
        system_prompt=bot.system_prompt,
        initial_message=bot.initial_message,
        avatar_url=bot.avatar_url,
        is_public=bot.is_public,
        created_at=bot.created_at,
    )


# Upload Avatar
@router.post("/bots/{bot_id}/avatar")
def upload_avatar(
    bot_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    bot = db.query(Bot).filter(Bot.id == bot_id).first()

    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")

    if bot.creator_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Generate unique filename
    file_ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_ext}"

    file_path = os.path.join(UPLOAD_DIR, filename)

    # Save file
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Save URL in DB
    bot.avatar_url = f"/uploads/avatars/{filename}"
    db.commit()

    return {"avatar_url": bot.avatar_url}


# List Bots
@router.get("/bots")
def list_bots(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    bots = db.query(Bot).filter(
        (Bot.is_public == True) |
        (Bot.creator_user_id == current_user.id)
    ).all()

    return [
        {
            "id": str(bot.id),
            "name": bot.name,
            "description": bot.description,
            "avatar_url": bot.avatar_url,
            "is_public": bot.is_public
        }
        for bot in bots
    ]


# Update Bot
@router.put("/bots/{bot_id}", response_model=BotResponse)
def update_bot(
    bot_id: str,
    request: BotUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    bot = db.query(Bot).filter(Bot.id == bot_id).first()

    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")

    if bot.creator_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if request.name is not None:
        bot.name = request.name

    if request.description is not None:
        bot.description = request.description

    if request.system_prompt is not None:
        bot.system_prompt = request.system_prompt

    if request.initial_message is not None:
        bot.initial_message = request.initial_message

    if request.is_public is not None:
        bot.is_public = request.is_public

    db.commit()
    db.refresh(bot)

    return BotResponse(
        id=str(bot.id),
        name=bot.name,
        description=bot.description,
        system_prompt=bot.system_prompt,
        initial_message=bot.initial_message,
        avatar_url=bot.avatar_url,
        is_public=bot.is_public,
        created_at=bot.created_at,
    )


# Delete Bot
@router.delete("/bots/{bot_id}")
def delete_bot(
    bot_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    bot = db.query(Bot).filter(Bot.id == bot_id).first()

    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")

    if bot.creator_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(bot)
    db.commit()

    return {"message": "Bot deleted successfully"}