from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.models import UserInteraction

router = APIRouter()

@router.post("/")
def chat_with_bot(user_input: dict, db: Session = Depends(get_db)):
    message = user_input.get("message", "").lower()

    # Simple intent classification
    if message in ["hello", "hi", "hey"]:
        intent = "Greeting"
        response_text = "Hi there! How can I assist you today?"
    else:
        intent = "General"
        response_text = f"Bot says: {message}"

    # Store in database
    interaction = UserInteraction(
        user_id="guest",
        query_text=message,
        intent=intent,
        response=response_text
    )
    db.add(interaction)
    db.commit()

    return {"response": response_text}

