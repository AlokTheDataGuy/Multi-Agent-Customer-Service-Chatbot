from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def place_order(order_data: dict):
    return {"message": "Order received!", "data": order_data}
