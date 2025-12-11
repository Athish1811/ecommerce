from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.session import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    carts = relationship("Cart", back_populates="user")
    
