from typing import Dict, List, Optional, Any
import re
from sqlalchemy.orm import Session
from app.database.models import Product, UserInteraction, Recommendation

class RecommendationAgent:
    """
    Recommendation Agent that offers personalized product recommendations
    based on user preferences and behavior.
    """

    def __init__(self, db: Optional[Session] = None):
        self.db = db

    def _extract_preferences(self, message: str) -> Dict[str, str]:
        """
        Extract user preferences from the message.

        Args:
            message: The user message

        Returns:
            Dictionary of extracted preferences
        """
        preferences = {}

        # Extract category preferences
        category_patterns = [
            r"(like|prefer|want|looking for) (a|an|some) ([\w\s]+) (product|item)",
            r"(interested in|searching for) ([\w\s]+)",
            r"(recommend|suggest) (a|an|some) ([\w\s]+)"
        ]

        for pattern in category_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match and match.lastindex:
                # Extract the category from the appropriate group
                if match.lastindex >= 3:
                    preferences['category'] = match.group(3).strip()
                elif match.lastindex >= 2:
                    preferences['category'] = match.group(2).strip()

        # Extract price range preferences
        price_patterns = [
            r"(under|less than|below|not more than) \$(\d+)",
            r"(around|about|approximately) \$(\d+)",
            r"(between) \$(\d+) and \$(\d+)",
            r"(more than|over|above) \$(\d+)"
        ]

        for pattern in price_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                price_type = match.group(1).lower()
                if price_type in ['under', 'less than', 'below', 'not more than']:
                    preferences['max_price'] = float(match.group(2))
                elif price_type in ['around', 'about', 'approximately']:
                    price = float(match.group(2))
                    preferences['min_price'] = price * 0.8  # 20% below
                    preferences['max_price'] = price * 1.2  # 20% above
                elif price_type == 'between' and match.lastindex >= 4:
                    preferences['min_price'] = float(match.group(2))
                    preferences['max_price'] = float(match.group(4))
                elif price_type in ['more than', 'over', 'above']:
                    preferences['min_price'] = float(match.group(2))

        # Extract feature preferences
        feature_patterns = [
            r"(with|has|having) ([\w\s]+)",
            r"(that is|that's|that are) ([\w\s]+)"
        ]

        for pattern in feature_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match and match.lastindex >= 2:
                preferences['features'] = match.group(2).strip()

        return preferences

    def _get_user_history(self, user_id: int) -> List[Dict]:
        """
        Get user's purchase and interaction history.

        Args:
            user_id: The user ID

        Returns:
            List of user's previous interactions and purchases
        """
        if not self.db:
            # Mock history for testing without DB
            return [
                {'product_id': 1, 'category': 'Electronics', 'interaction_type': 'view'},
                {'product_id': 2, 'category': 'Clothing', 'interaction_type': 'purchase'}
            ]

        # Get user's interactions from database
        interactions = self.db.query(UserInteraction).filter(UserInteraction.user_id == user_id).all()

        # Get user's recommendations from database
        recommendations = self.db.query(Recommendation).filter(Recommendation.user_id == user_id).all()

        history = []

        for interaction in interactions:
            history.append({
                'interaction_id': interaction.interaction_id,
                'query': interaction.query_text,
                'intent': interaction.intent,
                'timestamp': interaction.timestamp
            })

        for recommendation in recommendations:
            history.append({
                'recommendation_id': recommendation.recommendation_id,
                'product_id': recommendation.product_id,
                'rating': recommendation.rating,
                'timestamp': recommendation.timestamp
            })

        return history

    def _get_recommendations(self, preferences: Dict[str, str], user_id: Optional[int] = None) -> List[Dict]:
        """
        Get product recommendations based on user preferences and history.

        Args:
            preferences: Dictionary of user preferences
            user_id: The user ID (optional)

        Returns:
            List of recommended products
        """
        if not self.db:
            # Mock recommendations for testing without DB
            return [
                {
                    'product_id': 3,
                    'name': 'Recommended Product 1',
                    'category': preferences.get('category', 'Electronics'),
                    'price': 29.99,
                    'description': 'This is a recommended product based on your preferences.',
                    'match_score': 0.95
                },
                {
                    'product_id': 4,
                    'name': 'Recommended Product 2',
                    'category': preferences.get('category', 'Electronics'),
                    'price': 39.99,
                    'description': 'Another recommended product based on your preferences.',
                    'match_score': 0.85
                }
            ]

        # Build query based on preferences
        query = self.db.query(Product)

        if 'category' in preferences:
            query = query.filter(Product.category.ilike(f"%{preferences['category']}%"))

        if 'min_price' in preferences:
            query = query.filter(Product.price >= preferences['min_price'])

        if 'max_price' in preferences:
            query = query.filter(Product.price <= preferences['max_price'])

        # Get products matching the preferences
        products = query.limit(5).all()

        # Convert to list of dictionaries with match scores
        # In a real system, you would calculate actual match scores based on preferences and history
        recommendations = []
        for i, product in enumerate(products):
            match_score = 1.0 - (i * 0.1)  # Simple decreasing score for demonstration
            recommendations.append({
                'product_id': product.product_id,
                'name': product.name,
                'category': product.category,
                'price': product.price,
                'description': product.description,
                'match_score': match_score
            })

        return recommendations

    def _format_recommendations(self, recommendations: List[Dict]) -> str:
        """
        Format recommendations for display.

        Args:
            recommendations: List of recommended products

        Returns:
            Formatted recommendations string
        """
        if not recommendations:
            return "I couldn't find any products matching your preferences. Could you provide more details about what you're looking for?"

        result = "Based on your preferences, I recommend the following products:\n\n"

        for i, product in enumerate(recommendations, 1):
            result += f"{i}. **{product['name']}** (${product['price']:.2f})\n"
            result += f"   {product['description'][:100]}...\n"
            if 'match_score' in product:
                result += f"   Match: {int(product['match_score'] * 100)}%\n"
            result += "\n"

        result += "Would you like more details about any of these products?"

        return result

    def process(self, message: str, user_id: Optional[int] = None) -> Dict:
        """
        Process a user message and provide personalized recommendations.

        Args:
            message: The user message to process
            user_id: The user ID (optional)

        Returns:
            Dict containing:
                - 'response': The agent's response
                - 'recommendations': List of recommended products
        """
        # Extract user preferences from the message
        preferences = self._extract_preferences(message)

        # Get user history if user_id is provided
        history = self._get_user_history(user_id) if user_id else []

        # Get recommendations based on preferences and history
        recommendations = self._get_recommendations(preferences, user_id)

        # Format recommendations for display
        response = self._format_recommendations(recommendations)

        return {
            'response': response,
            'recommendations': recommendations
        }