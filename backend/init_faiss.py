import os
import pickle
import numpy as np
from app.utils.embeddings import get_embedding
from app.faiss.faiss_index import FAISSIndex

def init_faiss_index():
    """
    Initialize the FAISS index with sample data.
    """
    print("Initializing FAISS index with sample data...")
    
    # Create the directory if it doesn't exist
    os.makedirs('app/faiss', exist_ok=True)
    
    # Sample FAQs
    faqs = [
        {
            'id': 1,
            'question': 'What is your return policy?',
            'answer': 'You can return any product within 30 days of purchase for a full refund, provided the item is in its original condition.'
        },
        {
            'id': 2,
            'question': 'How long does shipping take?',
            'answer': 'Standard shipping takes 3-5 business days. Express shipping is available for an additional fee and takes 1-2 business days.'
        },
        {
            'id': 3,
            'question': 'Do you ship internationally?',
            'answer': 'Yes, we ship to most countries worldwide. International shipping typically takes 7-14 business days depending on the destination.'
        },
        {
            'id': 4,
            'question': 'How can I track my order?',
            'answer': 'You can track your order by logging into your account and viewing your order history, or by using the tracking number provided in your shipping confirmation email.'
        },
        {
            'id': 5,
            'question': 'Do you offer gift wrapping?',
            'answer': 'Yes, we offer gift wrapping for an additional $5 per item. You can select this option during checkout.'
        },
        {
            'id': 6,
            'question': 'What payment methods do you accept?',
            'answer': 'We accept all major credit cards (Visa, MasterCard, American Express), PayPal, and Apple Pay.'
        },
        {
            'id': 7,
            'question': 'Are there any discounts for bulk orders?',
            'answer': 'Yes, we offer discounts for orders of 10 or more items. Please contact our customer service for more information.'
        },
        {
            'id': 8,
            'question': 'How do I cancel an order?',
            'answer': 'You can cancel an order within 1 hour of placing it by contacting our customer service. After that, the order may have already been processed for shipping.'
        },
        {
            'id': 9,
            'question': 'Do you have a physical store?',
            'answer': 'Yes, we have physical stores in New York, Los Angeles, and Chicago. You can find the addresses and opening hours on our Contact page.'
        },
        {
            'id': 10,
            'question': 'Do you offer a warranty on your products?',
            'answer': 'Most of our products come with a 1-year manufacturer warranty. Please check the product description for specific warranty information.'
        }
    ]
    
    # Sample product descriptions
    products = [
        {
            'id': 1,
            'name': 'Wireless Headphones',
            'description': 'High-quality wireless headphones with noise cancellation and 20-hour battery life. Features Bluetooth 5.0 connectivity and comfortable over-ear design.',
            'category': 'Electronics',
            'price': 79.99
        },
        {
            'id': 2,
            'name': 'Cotton T-Shirt',
            'description': 'Comfortable 100% cotton t-shirt available in multiple colors. Pre-shrunk fabric and reinforced stitching for durability.',
            'category': 'Clothing',
            'price': 19.99
        },
        {
            'id': 3,
            'name': 'Smart Watch',
            'description': 'Feature-packed smartwatch with heart rate monitor, GPS, and 5-day battery life. Water-resistant up to 50 meters and compatible with iOS and Android.',
            'category': 'Electronics',
            'price': 149.99
        },
        {
            'id': 4,
            'name': 'Coffee Maker',
            'description': 'Programmable coffee maker with 12-cup capacity and built-in grinder. Features adjustable brew strength and keep-warm function.',
            'category': 'Home & Kitchen',
            'price': 89.99
        },
        {
            'id': 5,
            'name': 'Yoga Mat',
            'description': 'Non-slip yoga mat made from eco-friendly materials. 6mm thickness provides excellent cushioning and support for all types of yoga.',
            'category': 'Sports & Fitness',
            'price': 29.99
        }
    ]
    
    # Combine FAQs and products into a single list of documents
    documents = []
    
    # Add FAQs
    for faq in faqs:
        # Create a combined text for embedding
        text = f"{faq['question']} {faq['answer']}"
        documents.append({
            'id': f"faq_{faq['id']}",
            'text': text,
            'question': faq['question'],
            'answer': faq['answer'],
            'type': 'faq'
        })
    
    # Add products
    for product in products:
        # Create a combined text for embedding
        text = f"{product['name']} {product['description']} {product['category']}"
        documents.append({
            'id': f"product_{product['id']}",
            'text': text,
            'name': product['name'],
            'description': product['description'],
            'category': product['category'],
            'price': product['price'],
            'type': 'product'
        })
    
    # Generate embeddings for all documents
    print("Generating embeddings...")
    embeddings = []
    metadata = []
    
    for doc in documents:
        embedding = get_embedding(doc['text'])
        embeddings.append(embedding)
        metadata.append({k: v for k, v in doc.items() if k != 'text'})
    
    # Create and save the FAISS index
    print("Creating FAISS index...")
    index = FAISSIndex()
    index.add_data(embeddings, metadata)
    
    # Save the index
    print("Saving FAISS index...")
    index.save_index()
    
    print("FAISS index initialized successfully!")

if __name__ == "__main__":
    init_faiss_index()
