# E-Commerce Chatbot Backend

This is the backend for the E-Commerce Chatbot, a multi-agent system that provides customer service for an e-commerce platform.

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Initialize the database and FAISS index:
   ```
   python setup.py
   ```

3. Start the backend server:
   ```
   python main.py
   ```

The server will be available at http://localhost:8000.

## API Endpoints

- `/api/chat/` - Process chat messages through the agent pipeline
- `/api/order/` - Handle order operations
- `/api/recommend/` - Get product recommendations
- `/api/faq/` - Access frequently asked questions

## Architecture

The chatbot follows a pipeline architecture with specialized agents:

1. **Guard Agent** - Filters out irrelevant or inappropriate messages
2. **Classification Agent** - Determines user intent and routes to specialized agents
3. **Order Agent** - Guides users through the ordering process
4. **Details Agent** - Retrieves product information and answers FAQs
5. **Recommendation Agent** - Provides personalized product recommendations

## Database

The system uses SQLite for development and can be configured to use PostgreSQL in production by setting the `DATABASE_URL` environment variable.

## FAISS Index

The Details Agent uses a FAISS vector index for semantic search of FAQs and product information.
