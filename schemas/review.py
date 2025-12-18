from pydantic import BaseModel
class ReviewCreate(BaseModel):
    comment: str