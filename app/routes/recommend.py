from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.models import Recommendation, Product

router = APIRouter()

@router.get("/{user_id}")
def recommend_products(user_id: int, db: Session = Depends(get_db)):
    # Fetch recommendations for the user from the database
    recommendations = (
        db.query(Recommendation.product_id)
        .filter(Recommendation.user_id == user_id)
        .all()
    )

    # Extract product IDs from query result
    product_ids = [rec.product_id for rec in recommendations]

    # Fetch product details for recommended products
    recommended_products = (
        db.query(Product.name)
        .filter(Product.product_id.in_(product_ids))
        .all()
    )

    # Convert result to a list of product names
    recommended_product_names = [product.name for product in recommended_products]

    return {"recommendations": recommended_product_names}
