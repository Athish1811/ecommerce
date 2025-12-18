from pydantic import BaseModel

class MessageCreate(BaseModel):
    user_id: int
    title: str
    content: str
