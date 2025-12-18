from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

    reviews = relationship("Review", back_populates="user")
    payments = relationship("Payment", back_populates="user")  
    messages = relationship("Message", back_populates="user")
