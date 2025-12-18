from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.session import SessionLocal, engine,Base
from schemas.User import UserCreate,UserUpdate
from models.User import User
from routers.user_routes import userrouter
from routers.product_routes import productrouter
from routers.payment_routes import paymentrouter
from routers.review_routes import router
from routers.order_routes import orderrouter
from routers.inventory_routes import inventoryrouter
from routers.supplier_routes import supplierrouter
from routers.message_routes import messagerouter

app = FastAPI()
Base.metadata.create_all(bind=engine)
@app.get("/")
def greet():
    return {"message":"hello world"}

app.include_router(userrouter)
app.include_router(productrouter)
app.include_router(paymentrouter)
app.include_router(router)
app.include_router(orderrouter)
app.include_router(inventoryrouter)
app.include_router(supplierrouter)
app.include_router(messagerouter)





