from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from db.session import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    description = Column(Text)

    reviews = relationship("Review", back_populates="product", cascade="all, delete")
    inventory = relationship("Inventory", back_populates="product", uselist=False)
    order_items = relationship("OrderItem", back_populates="product")
