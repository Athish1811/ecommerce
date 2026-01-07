from fastapi import FastAPI
from db.session import engine, Base

from routers.user_routes import userrouter
from routers.product_routes import productrouter
from routers.payment_routes import paymentrouter
from routers.review_routes import router as reviewrouter

from routers.inventory_routes import inventoryrouter
from routers.supplier_routes import supplierrouter
from routers.message_routes import messagerouter
from routers.order_routes import order_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return {"message": "hello world"}

app.include_router(userrouter)
app.include_router(productrouter)
app.include_router(paymentrouter)
app.include_router(reviewrouter)

app.include_router(inventoryrouter)
app.include_router(supplierrouter)
app.include_router(messagerouter)
app.include_router(order_router)
