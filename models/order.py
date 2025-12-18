from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from db.session import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Integer)
    status = Column(String, default="PENDING")

    payment = relationship(
        "Payment",
        back_populates="order",
        uselist=False
    )
