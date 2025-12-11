from pydantic import BaseModel
from typing import Optional
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
   
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    