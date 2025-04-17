from app.database.db import engine, Base
from app.database.models import User, Order, Product, UserInteraction, FAQ, Recommendation, ChatLog
import json

def init_database():
    """
    Initialize the database with tables and sample data.
    """
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_database()
