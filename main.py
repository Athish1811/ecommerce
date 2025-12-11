from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.session import SessionLocal, engine,Base
from schemas.User import UserCreate,UserUpdate
from models.User import User
from routers.user_routes import userrouter
from routers.product_routes import productrouter
from routers.cart_routes import cartrouter
app = FastAPI()
Base.metadata.create_all(bind=engine)
@app.get("/")
def greet():
    return {"message":"hello world"}
app.include_router(userrouter)
app.include_router(productrouter)
app.include_router(cartrouter)
