from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.models import FAQ

router = APIRouter()

@router.get("/{question}")
def get_faq_answer(question: str, db: Session = Depends(get_db)):
    faq_entry = db.query(FAQ).filter(FAQ.question.ilike(f"%{question}%")).first()
    return {"answer": faq_entry.answer if faq_entry else "No answer found"}
