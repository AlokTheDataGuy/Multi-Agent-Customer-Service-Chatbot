from sqlalchemy import Column, Integer, String, JSON, Float, DateTime, Text, ForeignKey
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    order_status = Column(String, default="Pending", nullable=False)
    products = Column(Text, nullable=False)  # JSON string of product IDs & quantities
    total_price = Column(Float, nullable=False)
    payment_status = Column(String, nullable=False)  # Paid, Unpaid, Failed
    shipping_address = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    features = Column(Text, nullable=True)  # JSON string of key specifications
    image_url = Column(String, nullable=True)
    rating = Column(Float, nullable=True)
    reviews_count = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserInteraction(Base):
    __tablename__ = "user_interactions"

    interaction_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    query_text = Column(Text, nullable=False)
    intent = Column(String, nullable=False)  # Order, FAQ, Recommendation
    response = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class FAQ(Base):
    __tablename__ = "faqs"

    faq_id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(Text, unique=True, nullable=False)
    answer = Column(Text, nullable=False)

class Recommendation(Base):
    __tablename__ = "recommendations"

    recommendation_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    rating = Column(Float, nullable=True)  # User rating (if applicable)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class ChatLog(Base):
    __tablename__ = "chat_logs"

    chat_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    agent_name = Column(String, nullable=False)  # Guard, Order, Details, etc.
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
