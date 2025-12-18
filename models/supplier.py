from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.session import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    phone = Column(String)
    address = Column(String)

    supplies = relationship("SupplierSupply", back_populates="supplier")
