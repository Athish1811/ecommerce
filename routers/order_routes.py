from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from models.order import Order
from models.order_item import OrderItem
from schemas.order import OrderCreate, OrderResponse

order_router = APIRouter(prefix="/orders", tags=["Orders"])

@order_router.post("/", response_model=OrderResponse)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):

    order = Order(
        user_id=order_data.user_id,
        total_amount=order_data.total_amount
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    for item in order_data.items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(order_item)

    db.commit()
    db.refresh(order)
    return order



@order_router.get("/user/{user_id}", response_model=List[OrderResponse])
def get_orders_by_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(Order).filter(Order.user_id == user_id).all()


