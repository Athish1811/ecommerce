from pydantic import BaseModel

class SupplierCreate(BaseModel):
    name: str
    phone: str
    address: str

class SupplierSupplyCreate(BaseModel):
    supplier_id: int
    product_id: int
    quantity: int
