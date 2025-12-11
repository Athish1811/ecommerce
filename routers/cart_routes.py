from fastapi import FastAPI, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from dependencies import get_db
from models.User import User
from models.Product import Product
from models.Cart import Cart

cartrouter = APIRouter(prefix="/cart", tags=["Carts"])
@cartrouter.post("/add")
def add_to_cart(user_id: int, product_id: int, quantity: int = 1, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Check if product exists
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    # Create cart entry
    cart_item = Cart(
        user_id=user_id,
        product_id=product_id,
        
        quantity=quantity
    )
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return {"message": "Item added to cart"}

@cartrouter.get("/view/{user_id}")
def view_cart(user_id: int, db: Session = Depends(get_db)):

    
    query = text("""
        SELECT 
            cart.id AS cart_id,
            cart.product_id,
            cart.quantity,
            products.id AS prod_id,
            products.name AS product_name,
            products.price
        FROM cart
        JOIN products
            ON cart.product_id = products.id
        WHERE cart.user_id = :user_id
    """)

    results = db.execute(query, {"user_id": user_id}).fetchall()

    if not results:
        return {"message": "Cart is empty"}

    cart_items = []

    for row in results:
        cart_items.append({
            "cart_id": row[0],        # cart.id
            "product_id": row[1],     # cart.product_id
            "quantity": row[2],       # cart.quantity
            "product_name": row[4],   # products.name
            "price": row[5],          # products.price
            "total": row[5] * row[2]
        })

    return {
        "user_id": user_id,
        "items": cart_items
    }
