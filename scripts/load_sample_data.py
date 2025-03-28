# import json
# import os
# from sqlalchemy.orm import Session
# from app.database.db import SessionLocal, engine
# from app.database.models import User, UserInteraction, Order, FAQ, Product, Recommendation, ChatLog, Base

# # Ensure tables exist
# Base.metadata.create_all(bind=engine)

# def load_json(file_path):
#     """Loads JSON data from a file."""
#     with open(file_path, "r") as f:
#         return json.load(f)

# def insert_users(db: Session):
#     data = load_json("data/users_data.json")  # Load users from JSON
#     for item in data:
#         db.add(User(**item))
#     db.commit()
#     print("✅ Users inserted!")

# def insert_user_interactions(db: Session):
#     data = load_json("data/user_interaction.json")
#     for item in data:
#         db.add(UserInteraction(**item))
#     db.commit()
#     print("✅ User interactions inserted!")

# def insert_orders(db: Session):
#     data = load_json("data/order_data.json")
#     for item in data:
#         db.add(Order(**item))
#     db.commit()
#     print("✅ Orders inserted!")

# def insert_faqs(db: Session):
#     data = load_json("data/faq_data.json")
#     for item in data:
#         db.add(FAQ(**item))
#     db.commit()
#     print("✅ FAQs inserted!")

# def insert_products(db: Session):
#     data = load_json("data/product_data.json")
#     for item in data:
#         db.add(Product(**item))
#     db.commit()
#     print("✅ Products inserted!")

# def insert_recommendations(db: Session):
#     data = load_json("data/recommend.json")
#     for item in data:
#         db.add(Recommendation(**item))
#     db.commit()
#     print("✅ Recommendations inserted!")

# def insert_chat_logs(db: Session):
#     data = load_json("data/customer_support_chat_logs.json")
#     for item in data:
#         db.add(ChatLog(**item))
#     db.commit()
#     print("✅ Customer support chat logs inserted!")

# def main():
#     """Runs all database insert functions."""
#     db = SessionLocal()
#     try:
#         insert_users(db)  # Insert users first to avoid FK issues
#         insert_user_interactions(db)
#         insert_orders(db)
#         insert_faqs(db)
#         insert_products(db)
#         insert_recommendations(db)
#         insert_chat_logs(db)
#     finally:
#         db.close()

# if __name__ == "__main__":
#     main()
