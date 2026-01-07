from pydantic import BaseModel
from typing import List
from datetime import datetime


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    user_id: int
    total_amount: int
    items: List[OrderItemCreate]


class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int

    class Config:
        orm_mode = True

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: int
    status: str
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        orm_mode = True
