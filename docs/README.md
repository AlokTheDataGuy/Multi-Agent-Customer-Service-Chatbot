# Customer Service Chatbot (WIP)

## Overview
This is a **modular, agent-based customer service chatbot** for an e-commerce platform. The chatbot is designed to handle various customer interactions, including order processing, FAQs, and personalized recommendations. It is built using **FastAPI, LangChain, Llama3:1B, Ollama, PostgreSQL, FAISS, Docker, and Gradio**.

## Features
- **Guard Agent**: Filters and blocks inappropriate or irrelevant queries.
- **Order Taking Agent**: Uses chain-of-thought reasoning to guide customers through the order process.
- **Details Agent (RAG System)**: Retrieves and generates responses about menu details, allergens, and FAQs.
- **Recommendation Agent**: Provides personalized product recommendations based on user orders.
- **Classification Agent**: Routes queries to the appropriate agent based on intent classification.

## Tech Stack
- **Backend:** FastAPI
- **NLP & LLM:** LangChain, Llama3:1B, Ollama
- **Database:** PostgreSQL
- **Vector Store:** FAISS
- **Containerization:** Docker
- **Testing UI:** Gradio

## Architecture
The chatbot follows a **modular agent-based architecture**, where each agent has a specific role. The agents work together in a **pipeline architecture** to ensure smooth interactions.

## Installation
### Prerequisites
- Python 3.9+
- Docker
- PostgreSQL

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/AlokTheDataGuy/customer-service-chatbot.git
   cd customer-service-chatbot
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up PostgreSQL and FAISS.
4. Run the chatbot using Docker:
   ```sh
   docker-compose up --build
   ```
5. Access the Gradio UI for testing at `http://localhost:7860`

## Work in Progress
- Implementing **real-time query classification** for better routing.
- Fine-tuning **Llama3:1B** for improved response accuracy.
- Enhancing the **Recommendation Agent** with more personalization.
- Adding support for **multi-turn conversations**.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request.

## License
MIT License

---
Stay tuned for updates as we continue to improve the chatbot!

