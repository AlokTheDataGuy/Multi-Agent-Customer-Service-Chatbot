from fastapi import FastAPI
from app.routes import chat, order, recommend, faq

app = FastAPI(title="E-commerce Customer Service Chatbot")

# Include different routes
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(order.router, prefix="/order", tags=["Order"])
app.include_router(recommend.router, prefix="/recommend", tags=["Recommendation"])
app.include_router(faq.router, prefix="/faq", tags=["FAQ"])

@app.get("/")
def root():
    return {"message": "E-commerce Chatbot API is running!"}
