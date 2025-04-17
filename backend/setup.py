import os
import sys

def main():
    """
    Initialize the database and FAISS index.
    """
    print("Setting up the chatbot backend...")
    
    # Initialize the database
    print("\n1. Initializing the database...")
    try:
        import init_db
        init_db.main()
    except Exception as e:
        print(f"Error initializing database: {e}")
        return
    
    # Initialize the FAISS index
    print("\n2. Initializing the FAISS index...")
    try:
        import init_faiss
        init_faiss.init_faiss_index()
    except Exception as e:
        print(f"Error initializing FAISS index: {e}")
        return
    
    print("\n✅ Setup complete! You can now start the backend server with:")
    print("   python main.py")

if __name__ == "__main__":
    main()
