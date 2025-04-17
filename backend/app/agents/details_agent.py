from typing import Dict, List, Optional, Any
import re
from sqlalchemy.orm import Session
from app.database.models import Product, FAQ

class DetailsAgent:
    """
    Details Agent that retrieves and responds with detailed product information,
    including FAQs, allergens, and menu items.
    """

    def __init__(self, db: Optional[Session] = None, faiss_index=None):
        self.db = db
        # We're not using FAISS for now to simplify the implementation

    def _search_products(self, query: str) -> List[Dict]:
        """
        Search for products in the database based on a query.

        Args:
            query: The search query

        Returns:
            List of matching products
        """
        # Mock products for testing
        mock_products = [
            {
                'product_id': 1,
                'name': 'Wireless Headphones',
                'category': 'Electronics',
                'price': 79.99,
                'stock': 45,
                'description': 'High-quality wireless headphones with noise cancellation and 20-hour battery life.',
                'features': {'color': 'black', 'connectivity': 'Bluetooth 5.0'}
            },
            {
                'product_id': 2,
                'name': 'Cotton T-Shirt',
                'category': 'Clothing',
                'price': 19.99,
                'stock': 100,
                'description': 'Comfortable 100% cotton t-shirt available in multiple colors.',
                'features': {'material': 'cotton', 'sizes': 'S, M, L, XL'}
            },
            {
                'product_id': 3,
                'name': 'Smart Watch',
                'category': 'Electronics',
                'price': 149.99,
                'stock': 30,
                'description': 'Feature-packed smartwatch with heart rate monitor, GPS, and 5-day battery life.',
                'features': {'water_resistant': 'Yes', 'compatibility': 'iOS and Android'}
            },
            {
                'product_id': 4,
                'name': 'Coffee Maker',
                'category': 'Home & Kitchen',
                'price': 89.99,
                'stock': 25,
                'description': 'Programmable coffee maker with 12-cup capacity and built-in grinder.',
                'features': {'capacity': '12 cups', 'programmable': 'Yes'}
            }
        ]

        # Filter products based on the query
        if not query or query.lower() in ['hi', 'hello', 'hey', 'hii']:
            # Return all products for generic greetings
            return mock_products[:2]  # Just return a couple to keep it simple

        # Simple search implementation
        results = []
        query_lower = query.lower()
        for product in mock_products:
            if (query_lower in product['name'].lower() or
                query_lower in product['category'].lower() or
                query_lower in product['description'].lower()):
                results.append(product)

        return results if results else mock_products[:1]  # Return at least one product

    def _search_faqs(self, query: str) -> List[Dict]:
        """
        Search for FAQs based on a query.

        Args:
            query: The search query

        Returns:
            List of matching FAQs
        """
        # Mock FAQs for testing
        mock_faqs = [
            {
                'faq_id': 1,
                'question': 'What is your return policy?',
                'answer': 'You can return any product within 30 days of purchase for a full refund.'
            },
            {
                'faq_id': 2,
                'question': 'How long does shipping take?',
                'answer': 'Standard shipping takes 3-5 business days. Express shipping is available for an additional fee.'
            },
            {
                'faq_id': 3,
                'question': 'Do you ship internationally?',
                'answer': 'Yes, we ship to most countries worldwide. International shipping typically takes 7-14 business days.'
            }
        ]

        # Filter FAQs based on the query
        if not query or query.lower() in ['hi', 'hello', 'hey', 'hii']:
            # Return a generic FAQ for greetings
            return [mock_faqs[0]]

        # Simple search implementation
        results = []
        query_lower = query.lower()
        for faq in mock_faqs:
            if (query_lower in faq['question'].lower() or
                query_lower in faq['answer'].lower()):
                results.append(faq)

        return results if results else [mock_faqs[0]]  # Return at least one FAQ

    def _format_product_info(self, product: Dict) -> str:
        """
        Format product information for display.

        Args:
            product: Product information dictionary

        Returns:
            Formatted product information string
        """
        result = f"**{product['name']}**\n\n"
        result += f"**Category:** {product['category']}\n"
        result += f"**Price:** ${product['price']:.2f}\n"
        result += f"**Availability:** {'In Stock' if product['stock'] > 0 else 'Out of Stock'}\n\n"
        result += f"**Description:**\n{product['description']}\n\n"

        if product.get('features') and isinstance(product['features'], dict):
            result += "**Features:**\n"
            for key, value in product['features'].items():
                result += f"- {key.capitalize()}: {value}\n"

        return result

    def _generate_response(self, query: str, products: List[Dict], faqs: List[Dict]) -> str:
        """
        Generate a response based on the query and search results.

        Args:
            query: The search query
            products: List of matching products
            faqs: List of matching FAQs

        Returns:
            Generated response string
        """
        # Handle greetings
        if query.lower() in ['hi', 'hello', 'hey', 'hii']:
            return "Hello! How can I help you today? You can ask about our products, shipping, or return policy."

        response = ""

        # Add product information
        if products:
            if len(products) == 1:
                response += f"Here's the information about {products[0]['name']}:\n\n"
                response += self._format_product_info(products[0])
            else:
                response += f"I found {len(products)} products that match your query:\n\n"
                for i, product in enumerate(products, 1):
                    response += f"{i}. **{product['name']}** - ${product['price']:.2f}\n"
                response += "\nPlease specify which product you'd like more information about."

        # Add FAQ information if available and not too many products
        if faqs and (len(products) <= 1):
            if response:
                response += "\n\n**Related FAQs:**\n\n"

            for faq in faqs:
                response += f"**Q: {faq['question']}**\n"
                response += f"A: {faq['answer']}\n\n"

        # If no response was generated, provide a fallback
        if not response:
            response = f"I couldn't find specific information about '{query}'. Please try asking about our products, shipping, or return policy."

        return response

    def process(self, message: str) -> Dict:
        """
        Process a user message and retrieve relevant product information.

        Args:
            message: The user message to process

        Returns:
            Dict containing:
                - 'response': The agent's response
                - 'products': List of matching products
                - 'faqs': List of matching FAQs
        """
        # Use the message as the query
        query = message.strip()

        # Search for matching products and FAQs
        products = self._search_products(query)
        faqs = self._search_faqs(query)

        # Generate a response based on the search results
        response = self._generate_response(query, products, faqs)

        return {
            'response': response,
            'products': products,
            'faqs': faqs
        }