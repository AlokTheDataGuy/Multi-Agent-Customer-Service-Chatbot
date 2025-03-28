from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.models import Order

router = APIRouter()

@router.post("/")
def place_order(order_data: dict, db: Session = Depends(get_db)):
    new_order = Order(
        user_id=order_data["user_id"],
        products=order_data["products"],
        total_price=order_data["total_price"],
        order_status="Pending",
        payment_status=order_data.get("payment_status", "Unpaid"),  # Default to Unpaid
        shipping_address=order_data["shipping_address"]  # Required field
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)  # Refresh to get generated values like `order_id`

    return {
        "message": "Order placed successfully",
        "order_id": new_order.order_id,  # Use `order_id` instead of `id`
        "order_status": new_order.order_status,
        "payment_status": new_order.payment_status
    }
