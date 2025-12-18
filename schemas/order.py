from pydantic import BaseModel

class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int
