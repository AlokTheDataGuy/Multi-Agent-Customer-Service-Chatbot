# E-Commerce Customer Service Chatbot

A multi-agent customer service chatbot for an e-commerce platform that can filter messages, classify user intent, guide users through ordering, retrieve product information, and offer personalized recommendations.

## Architecture

The system follows a modular pipeline structure:

```
User ->
Guard Agent ->
Classification Agent ->
   -> Order Taking Agent
   -> Details Agent
   -> Recommendation Agent
Back to User
```

## Features

- **Guard Agent**: Filters out irrelevant or inappropriate messages before processing
- **Classification Agent**: Accurately classifies user intent and routes queries to specialized agents
- **Order Taking Agent**: Guides users through the ordering process using step-by-step reasoning
- **Details Agent**: Retrieves and responds with detailed product information (RAG System)
- **Recommendation Agent**: Offers personalized product recommendations based on user preferences

## Tech Stack

### Backend
- Python 3.9+
- FastAPI
- SQLAlchemy
- PostgreSQL
- FAISS for vector search
- Hugging Face Transformers

### Frontend
- React
- React Router
- Axios

## Project Structure

```
├── backend/             # Backend code
│   ├── app/            # FastAPI application
│   │   ├── agents/     # Agent implementations
│   │   ├── database/   # Database models and connection
│   │   ├── faiss/      # Vector search implementation
│   │   ├── routes/     # API endpoints
│   │   ├── services/   # Business logic services
│   │   └── utils/      # Utility functions
│   ├── main.py         # Entry point for the backend
│   └── requirements.txt # Python dependencies
│
└── frontend/           # React frontend
    ├── public/         # Static files
    ├── src/            # React source code
    │   ├── components/ # Reusable UI components
    │   ├── pages/      # Page components
    │   └── services/   # API services
    └── package.json    # Node.js dependencies
```

## Setup and Installation

### Prerequisites
- Python 3.9+
- Node.js and npm
- PostgreSQL

### Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/customer-service-chatbot.git
cd customer-service-chatbot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

4. Set up environment variables by creating a `.env` file in the backend directory:
```
DATABASE_URL=postgresql://username:password@localhost:5432/ecommerce_chatbot
```

### Database Setup

1. Create a PostgreSQL database:
```bash
createdb ecommerce_chatbot
```

2. Run database migrations (if applicable)

### Running the Application

You can use the provided scripts to start the application:

#### On Linux/Mac:

```bash
# Start both backend and frontend
./run.sh

# Start only the backend
./run.sh backend

# Start only the frontend
./run.sh frontend

# Build the frontend
./run.sh build
```

#### On Windows:

```cmd
# Start both backend and frontend
run.bat

# Start only the backend
run.bat backend

# Start only the frontend
run.bat frontend

# Build the frontend
run.bat build
```

Alternatively, you can start the services manually:

#### Backend

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:5173

### Building for Production

1. Build the React frontend:
```bash
cd frontend
npm run build
```

2. Start the production server:
```bash
cd backend
python -m uvicorn app.main:app
```

The application will serve both the API and the frontend from http://localhost:8000

## API Endpoints

- `/api/chat/` - Process chat messages
- `/api/order/` - Handle order operations
- `/api/recommend/` - Get product recommendations
- `/api/faq/` - Access frequently asked questions

## License

[MIT License](LICENSE)
