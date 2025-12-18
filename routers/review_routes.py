from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models.review import Review
from models.Product import Product
from schemas.review import ReviewCreate
router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)

@router.post("/add/{user_id}/{product_id}")
def add_review(
    user_id: int,
    product_id: int,
    review: ReviewCreate,
    db: Session = Depends(get_db)
):
    new_review = Review(
        user_id=user_id,
        product_id=product_id,
        comment=review.comment
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return {
        "message": "Review added successfully",
        "review_id": new_review.id,
        "comment": new_review.comment
    }

@router.get("/view/{user_id}")
def view_reviews(user_id: int, db: Session = Depends(get_db)):
    data = (
        db.query(Review, Product)
        .join(Product, Review.product_id == Product.id) 
        .filter(Review.user_id == user_id)
        .all()
    )
    if not data:
        return {"message": "No reviews found"}
    reviews = []
    for review, product in data:
        reviews.append({
            "review_id": review.id,
            "product_id": product.id,
            "product_name": product.name,
            "comment": review.comment
        })
    return {
        "user_id": user_id,
        "reviews": reviews
    }