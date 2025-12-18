from pydantic import BaseModel

class InventoryCreate(BaseModel):
    product_id: int
    quantity: int

class InventoryUpdate(BaseModel):
    quantity: int
