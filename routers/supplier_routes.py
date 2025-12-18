from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models.supplier import Supplier
from models.supplier_supply import SupplierSupply
from models.inventory import Inventory
from models.Product import Product
from schemas.supplier import SupplierCreate, SupplierSupplyCreate

supplierrouter = APIRouter(
    prefix="/supplier",
    tags=["Supplier"]
)

@supplierrouter.post("/add")
def add_supplier(data: SupplierCreate, db: Session = Depends(get_db)):
    supplier = Supplier(**data.dict())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier


@supplierrouter.get("/")
def get_suppliers(db: Session = Depends(get_db)):
    return db.query(Supplier).all()

@supplierrouter.post("/supply")
def supplier_supply(data: SupplierSupplyCreate, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(
        Supplier.id == data.supplier_id
    ).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    product = db.query(Product).filter(
        Product.id == data.product_id
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    supply = SupplierSupply(**data.dict())
    db.add(supply)


    inventory = db.query(Inventory).filter(
        Inventory.product_id == data.product_id
    ).first()

    if inventory:
        inventory.quantity += data.quantity
    else:
        inventory = Inventory(
            product_id=data.product_id,
            quantity=data.quantity
        )
        db.add(inventory)

    db.commit()
    return {"message": "Stock added from supplier"}
