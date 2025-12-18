from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models.payment import Payment
from models.order import Order
from schemas.payment import PaymentCreate

paymentrouter = APIRouter(
    prefix="/payment",
    tags=["Payment"]
)

@paymentrouter.post("/pay")
def pay_order(data: PaymentCreate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == data.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status == "PAID":
        raise HTTPException(status_code=400, detail="Order already paid")

    payment = Payment(
        order_id=order.id,
        amount=order.total_amount,
        method=data.payment_method
    )

    order.status = "PAID"

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return {
        "message": "Payment successful",
        "payment_id": payment.id,
        "order_id": order.id,
        "amount": payment.amount
    }
