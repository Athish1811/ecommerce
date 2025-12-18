from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.session import Base

class SupplierSupply(Base):
    __tablename__ = "supplier_supplies"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)

    supplier = relationship("Supplier", back_populates="supplies")
    product = relationship("Product")
