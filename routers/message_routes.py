from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models.message import Message
from models.User import User
from schemas.message import MessageCreate

messagerouter = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)


@messagerouter.post("/")
def create_message(data: MessageCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    message = Message(**data.dict())
    db.add(message)
    db.commit()
    db.refresh(message)
    return {"message": "Notification created"}

@messagerouter.get("/{user_id}")
def get_user_messages(user_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Message)
        .filter(Message.user_id == user_id)
        .order_by(Message.created_at.desc())
        .all()
    )


@messagerouter.put("/{message_id}/read")
def mark_as_read(message_id: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    message.is_read = True
    db.commit()
    return {"message": "Marked as read"}
