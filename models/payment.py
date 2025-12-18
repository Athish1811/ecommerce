from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from db.session import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))
    amount = Column(Integer)
    status = Column(String, default="INITIATED")

    user = relationship("User", back_populates="payments")
    order = relationship("Order", back_populates="payment")
