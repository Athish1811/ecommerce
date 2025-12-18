from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models.inventory import Inventory
from models.Product import Product
from schemas.inventory import InventoryCreate, InventoryUpdate

inventoryrouter = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)

@inventoryrouter.get("/")
def get_all_inventory(db: Session = Depends(get_db)):
    return db.query(Inventory).all()

@inventoryrouter.get("/{product_id}")
def get_inventory(product_id: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(
        Inventory.product_id == product_id
    ).first()

    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")

    return inventory

@inventoryrouter.post("/add")
def add_inventory(data: InventoryCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing = db.query(Inventory).filter(
        Inventory.product_id == data.product_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Inventory already exists")

    inventory = Inventory(
        product_id=data.product_id,
        quantity=data.quantity
    )

    db.add(inventory)
    db.commit()
    db.refresh(inventory)

    return {"message": "Inventory added", "inventory": inventory}

@inventoryrouter.put("/update/{product_id}")
def update_inventory(
    product_id: int,
    data: InventoryUpdate,
    db: Session = Depends(get_db)
):
    inventory = db.query(Inventory).filter(
        Inventory.product_id == product_id
    ).first()

    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")

    inventory.quantity = data.quantity
    db.commit()
    db.refresh(inventory)

    return {"message": "Inventory updated", "inventory": inventory}
