from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models.order import Order
from models.Product import Product
from models.User import User
from schemas.order import OrderCreate

orderrouter = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@orderrouter.post("/create")
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    total = product.price * data.quantity

    order = Order(
        user_id=data.user_id,
        product_id=data.product_id,
        quantity=data.quantity,
        total_amount=total
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return {
        "message": "Order created",
        "order_id": order.id,
        "total_amount": order.total_amount,
        "status": order.status
    }

@orderrouter.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return {"message": "Order not found"}

    return {
        "order_id": order.id,
        "user_id": order.user_id,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "total_amount": order.total_amount,
        "status": order.status,
        "created_at": order.created_at
    }

@orderrouter.get("/user/{user_id}")
def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == user_id).all()

    if not orders:
        return {"message": "No orders found"}

    return orders

