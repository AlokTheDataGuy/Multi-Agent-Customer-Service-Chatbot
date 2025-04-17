import json
import os
import sys
import sqlite3
from sqlalchemy.orm import Session
from app.database.db import SessionLocal, engine
from app.database.models import User, UserInteraction, Order, FAQ, Product, Recommendation, ChatLog, Base

# Ensure tables exist
Base.metadata.create_all(bind=engine)

def load_json(file_path):
    """Loads JSON data from a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        print(f"Current working directory: {os.getcwd()}")
        print("Please make sure the data files are in the correct location.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file: {file_path}")
        sys.exit(1)

def insert_users(db: Session):
    try:
        data = load_json("../data/users_data.json")  # Load users from JSON
        for item in data:
            # Ensure required fields are present
            if 'name' not in item or 'email' not in item or 'password_hash' not in item:
                print(f"Warning: Skipping user with missing required fields: {item}")
                continue
            
            # Check if user already exists
            existing_user = db.query(User).filter(User.email == item['email']).first()
            if existing_user:
                print(f"User with email {item['email']} already exists, skipping.")
                continue
                
            db.add(User(**item))
        db.commit()
        print("✅ Users inserted!")
    except Exception as e:
        db.rollback()
        print(f"❌ Error inserting users: {e}")

def insert_user_interactions(db: Session):
    try:
        data = load_json("../data/user_interaction.json")
        for item in data:
            # Ensure required fields are present
            if 'user_id' not in item or 'query_text' not in item or 'intent' not in item or 'response' not in item:
                print(f"Warning: Skipping interaction with missing required fields: {item}")
                continue
                
            db.add(UserInteraction(**item))
        db.commit()
        print("✅ User interactions inserted!")
    except Exception as e:
        db.rollback()
        print(f"❌ Error inserting user interactions: {e}")

def insert_orders(db: Session):
    try:
        data = load_json("../data/order_data.json")
        for item in data:
            # Convert products to JSON string for SQLite
            if 'products' in item and isinstance(item['products'], (dict, list)):
                item['products'] = json.dumps(item['products'])
                
            # Ensure required fields are present
            required_fields = ['user_id', 'order_status', 'products', 'total_price', 
                              'payment_status', 'shipping_address']
            if not all(field in item for field in required_fields):
                print(f"Warning: Skipping order with missing required fields: {item}")
                continue
                
            db.add(Order(**item))
        db.commit()
        print("✅ Orders inserted!")
    except Exception as e:
        db.rollback()
        print(f"❌ Error inserting orders: {e}")

def insert_faqs(db: Session):
    try:
        data = load_json("../data/faq_data.json")
        for item in data:
            # Ensure required fields are present
            if 'question' not in item or 'answer' not in item:
                print(f"Warning: Skipping FAQ with missing required fields: {item}")
                continue
                
            db.add(FAQ(**item))
        db.commit()
        print("✅ FAQs inserted!")
    except Exception as e:
        db.rollback()
        print(f"❌ Error inserting FAQs: {e}")

def insert_products(db: Session):
    try:
        data = load_json("../data/product_data.json")
        for item in data:
            # Convert features to JSON string for SQLite
            if 'features' in item and isinstance(item['features'], (dict, list)):
                item['features'] = json.dumps(item['features'])
                
            # Ensure required fields are present
            required_fields = ['name', 'category', 'price', 'stock', 'description']
            if not all(field in item for field in required_fields):
                print(f"Warning: Skipping product with missing required fields: {item}")
                continue
                
            db.add(Product(**item))
        db.commit()
        print("✅ Products inserted!")
    except Exception as e:
        db.rollback()
        print(f"❌ Error inserting products: {e}")

def insert_recommendations(db: Session):
    try:
        data = load_json("../data/recommend.json")
        for item in data:
            # Ensure required fields are present
            if 'user_id' not in item or 'product_id' not in item:
                print(f"Warning: Skipping recommendation with missing required fields: {item}")
                continue
                
            db.add(Recommendation(**item))
        db.commit()
        print("✅ Recommendations inserted!")
    except Exception as e:
        db.rollback()
        print(f"❌ Error inserting recommendations: {e}")

def insert_chat_logs(db: Session):
    try:
        data = load_json("../data/customer_support_chat_logs.json")
        for item in data:
            # Ensure required fields are present
            required_fields = ['user_id', 'agent_name', 'message', 'response']
            if not all(field in item for field in required_fields):
                print(f"Warning: Skipping chat log with missing required fields: {item}")
                continue
                
            db.add(ChatLog(**item))
        db.commit()
        print("✅ Customer support chat logs inserted!")
    except Exception as e:
        db.rollback()
        print(f"❌ Error inserting chat logs: {e}")

def main():
    """Runs all database insert functions."""
    print("Initializing database...")
    
    # Create database file if it doesn't exist
    if not os.path.exists("test.db"):
        print("Creating new SQLite database file...")
    
    db = SessionLocal()
    try:
        # Insert data in order to avoid foreign key constraint issues
        insert_users(db)  # Insert users first to avoid FK issues
        insert_products(db)  # Insert products before recommendations
        insert_faqs(db)
        insert_orders(db)
        insert_user_interactions(db)
        insert_recommendations(db)
        insert_chat_logs(db)
        
        print("\nDatabase initialization complete! ✨")
    except Exception as e:
        print(f"Error during database initialization: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
