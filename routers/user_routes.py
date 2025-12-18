from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from models.User import User
from models.Product import Product
from models.payment import Payment
from schemas.User import UserCreate,UserUpdate
from dependencies import get_db
userrouter = APIRouter(
    prefix="/users",
    tags=["Users"]
)
@userrouter.post("/signup")
def signup(user:UserCreate, db:Session=Depends(get_db)):
    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)    
    return new_user

@userrouter.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return user
    return {"message": "User not found"}

@userrouter.put("/{user_id}")
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.username = user_update.username
        user.email = user_update.email
        db.commit()
        db.refresh(user)
        return {"message":"Update Done",**user}
    return {"message": "User not found"}

@userrouter.delete("/")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
    return {"message": "User not found"}

@userrouter.get("/users/{user_id}/cart")
def get_user_cart(user_id: int, db: Session = Depends(get_db)):
    data = (
        db.query(Cart, Product)
        .join(Product, Cart.product_id == Product.id)
        .filter(Cart.user_id == user_id)
        .all()
    )

    result = []
    for cart_item, product in data:
        result.append({
            "product": product.name,
            "price": product.price,
            "quantity": cart_item.quantity
        })
    return result   