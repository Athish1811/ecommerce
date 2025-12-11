from fastapi import FastAPI, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
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
    results = (
        db.query(Cart, Product)
        .join(Product, Cart.product_id == Product.id)
        .filter(Cart.user_id == user_id)
        .all()
    )
    print(results)
    if not results:
        return {"message": "Cart is empty"}

    cart_items = []
    for cart_row, product_row in results:
        cart_items.append({
            "cart_id": cart_row.id,
            "product_id": product_row.id,
            "product_name": product_row.name,
            "price": product_row.price,
            "quantity": cart_row.quantity,
            "total": product_row.price * cart_row.quantity
        })

    return {
        "user_id": user_id,
        "items": cart_items
    }
