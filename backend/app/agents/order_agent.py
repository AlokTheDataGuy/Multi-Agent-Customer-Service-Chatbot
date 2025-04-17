from typing import Dict, List, Optional, Any
import re
from sqlalchemy.orm import Session
from app.database.models import Product, Order, User

class OrderAgent:
    """
    Order Agent that guides users through the ordering process
    using step-by-step reasoning.
    """

    def __init__(self, db: Optional[Session] = None):
        self.db = db
        self.order_states = {
            'init': self._handle_init,
            'product_selection': self._handle_product_selection,
            'quantity_selection': self._handle_quantity_selection,
            'address_collection': self._handle_address_collection,
            'payment_method': self._handle_payment_method,
            'confirmation': self._handle_confirmation,
            'complete': self._handle_complete
        }

    def _extract_product_name(self, message: str) -> Optional[str]:
        """
        Extract product name from user message.

        Args:
            message: The user message

        Returns:
            Extracted product name or None if not found
        """
        # Simple extraction based on common patterns
        patterns = [
            r"I want to (order|buy|get|purchase) (a|an|some) ([\w\s]+)",
            r"I('|')d like to (order|buy|get|purchase) (a|an|some) ([\w\s]+)",
            r"Can I (order|buy|get|purchase) (a|an|some) ([\w\s]+)",
            r"(order|buy|get|purchase) (a|an|some) ([\w\s]+)"
        ]

        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                # The product name will be in the last group
                return match.group(match.lastindex).strip()

        return None

    def _extract_quantity(self, message: str) -> Optional[int]:
        """
        Extract quantity from user message.

        Args:
            message: The user message

        Returns:
            Extracted quantity or None if not found
        """
        # Look for numbers in the message
        quantity_patterns = [
            r"(\d+) (of them|items|products|pieces)",
            r"quantity (of|is) (\d+)",
            r"(\d+) (please|thanks|thank you)",
            r"^(\d+)$"
        ]

        for pattern in quantity_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                for group in match.groups():
                    if group and group.isdigit():
                        return int(group)

        # Check for written numbers
        written_numbers = {
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
        }

        for word, number in written_numbers.items():
            if re.search(r'\b' + word + r'\b', message, re.IGNORECASE):
                return number

        return None

    def _extract_address(self, message: str) -> Optional[str]:
        """
        Extract address from user message.

        Args:
            message: The user message

        Returns:
            Extracted address or None if not valid
        """
        # Simple validation - check if the message is long enough to be an address
        if len(message.strip()) > 10 and any(char.isdigit() for char in message):
            return message.strip()
        return None

    def _extract_payment_method(self, message: str) -> Optional[str]:
        """
        Extract payment method from user message.

        Args:
            message: The user message

        Returns:
            Extracted payment method or None if not valid
        """
        payment_methods = {
            'credit': 'credit_card',
            'credit card': 'credit_card',
            'debit': 'debit_card',
            'debit card': 'debit_card',
            'paypal': 'paypal',
            'cash': 'cash_on_delivery',
            'cash on delivery': 'cash_on_delivery',
            'cod': 'cash_on_delivery'
        }

        message_lower = message.lower()
        for key, value in payment_methods.items():
            if key in message_lower:
                return value

        return None

    def _get_product_by_name(self, product_name: str) -> Optional[Dict]:
        """
        Get product details by name from the database.

        Args:
            product_name: The name of the product to search for

        Returns:
            Product details as a dictionary or None if not found
        """
        if not self.db:
            # Mock product for testing without DB
            return {
                'product_id': 1,
                'name': product_name,
                'price': 19.99,
                'stock': 100,
                'description': f"This is a {product_name}"
            }

        # Search for product in database
        product = self.db.query(Product).filter(Product.name.ilike(f'%{product_name}%')).first()

        if product:
            return {
                'product_id': product.product_id,
                'name': product.name,
                'price': product.price,
                'stock': product.stock,
                'description': product.description
            }

        return None

    def _handle_init(self, message: str, context: Dict) -> Dict:
        """
        Handle initial state of the order process.

        Args:
            message: The user message
            context: The current context of the conversation

        Returns:
            Updated context and response
        """
        product_name = self._extract_product_name(message)

        if product_name:
            product = self._get_product_by_name(product_name)

            if product:
                context['product'] = product
                context['state'] = 'quantity_selection'
                return {
                    'context': context,
                    'response': f"I found {product['name']}. It costs ${product['price']:.2f}. How many would you like to order?"
                }
            else:
                return {
                    'context': context,
                    'response': f"I couldn't find a product called '{product_name}'. Could you please specify a different product?"
                }

        return {
            'context': context,
            'response': "What product would you like to order today?"
        }

    def _handle_product_selection(self, message: str, context: Dict) -> Dict:
        """
        Handle product selection state.

        Args:
            message: The user message
            context: The current context of the conversation

        Returns:
            Updated context and response
        """
        product_name = self._extract_product_name(message)

        if product_name:
            product = self._get_product_by_name(product_name)

            if product:
                context['product'] = product
                context['state'] = 'quantity_selection'
                return {
                    'context': context,
                    'response': f"Great! You've selected {product['name']}. It costs ${product['price']:.2f}. How many would you like to order?"
                }
            else:
                return {
                    'context': context,
                    'response': f"I couldn't find a product called '{product_name}'. Could you please specify a different product?"
                }

        return {
            'context': context,
            'response': "I didn't catch which product you want. Could you please specify the product name?"
        }

    def _handle_quantity_selection(self, message: str, context: Dict) -> Dict:
        """
        Handle quantity selection state.

        Args:
            message: The user message
            context: The current context of the conversation

        Returns:
            Updated context and response
        """
        quantity = self._extract_quantity(message)

        if quantity:
            if quantity <= 0:
                return {
                    'context': context,
                    'response': "The quantity must be greater than zero. How many would you like to order?"
                }

            product = context.get('product', {})
            if product.get('stock', 0) < quantity:
                return {
                    'context': context,
                    'response': f"I'm sorry, we only have {product.get('stock', 0)} units in stock. Please select a smaller quantity."
                }

            context['quantity'] = quantity
            context['state'] = 'address_collection'

            total_price = product.get('price', 0) * quantity
            context['total_price'] = total_price

            return {
                'context': context,
                'response': f"You've selected {quantity} x {product.get('name', '')}. Your total is ${total_price:.2f}. Please provide your delivery address."
            }

        return {
            'context': context,
            'response': "I need to know how many you'd like to order. Please provide a quantity."
        }

    def _handle_address_collection(self, message: str, context: Dict) -> Dict:
        """
        Handle address collection state.

        Args:
            message: The user message
            context: The current context of the conversation

        Returns:
            Updated context and response
        """
        address = self._extract_address(message)

        if address:
            context['address'] = address
            context['state'] = 'payment_method'

            return {
                'context': context,
                'response': "Thanks for providing your address. How would you like to pay? We accept credit card, debit card, PayPal, or cash on delivery."
            }

        return {
            'context': context,
            'response': "I need a valid delivery address to proceed with your order. Please provide your full address including street, city, and zip code."
        }

    def _handle_payment_method(self, message: str, context: Dict) -> Dict:
        """
        Handle payment method selection state.

        Args:
            message: The user message
            context: The current context of the conversation

        Returns:
            Updated context and response
        """
        payment_method = self._extract_payment_method(message)

        if payment_method:
            context['payment_method'] = payment_method
            context['state'] = 'confirmation'

            product = context.get('product', {})
            quantity = context.get('quantity', 0)
            total_price = context.get('total_price', 0)
            address = context.get('address', '')

            return {
                'context': context,
                'response': f"Great! Here's a summary of your order:\n\n" +
                           f"Product: {product.get('name', '')}\n" +
                           f"Quantity: {quantity}\n" +
                           f"Total Price: ${total_price:.2f}\n" +
                           f"Delivery Address: {address}\n" +
                           f"Payment Method: {payment_method}\n\n" +
                           f"Would you like to confirm this order?"
            }

        return {
            'context': context,
            'response': "Please select a valid payment method. We accept credit card, debit card, PayPal, or cash on delivery."
        }

    def _handle_confirmation(self, message: str, context: Dict) -> Dict:
        """
        Handle order confirmation state.

        Args:
            message: The user message
            context: The current context of the conversation

        Returns:
            Updated context and response
        """
        confirmation_patterns = [
            r'\b(yes|yeah|yep|confirm|proceed|ok|okay|sure|go ahead)\b'
        ]

        rejection_patterns = [
            r'\b(no|nope|cancel|stop|don\'t|do not)\b'
        ]

        for pattern in confirmation_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                # Create order in database if DB is available
                if self.db:
                    new_order = Order(
                        user_id=context.get('user_id', 1),  # Default user ID if not provided
                        order_status='Pending',
                        products={
                            'product_id': context.get('product', {}).get('product_id', 0),
                            'quantity': context.get('quantity', 0)
                        },
                        total_price=context.get('total_price', 0),
                        payment_status='Unpaid',
                        shipping_address=context.get('address', '')
                    )
                    self.db.add(new_order)
                    self.db.commit()
                    context['order_id'] = new_order.order_id
                else:
                    # Mock order ID for testing without DB
                    context['order_id'] = 12345

                context['state'] = 'complete'
                return {
                    'context': context,
                    'response': f"Thank you! Your order has been confirmed. Your order ID is #{context['order_id']}. You will receive a confirmation email shortly."
                }

        for pattern in rejection_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                context['state'] = 'init'
                return {
                    'context': context,
                    'response': "I've canceled your order. Is there anything else you'd like to order?"
                }

        return {
            'context': context,
            'response': "I didn't understand your response. Please confirm with 'yes' or cancel with 'no'."
        }

    def _handle_complete(self, message: str, context: Dict) -> Dict:
        """
        Handle completed order state.

        Args:
            message: The user message
            context: The current context of the conversation

        Returns:
            Updated context and response
        """
        # Reset the state for a new order
        new_context = {'state': 'init'}

        return {
            'context': new_context,
            'response': "Your order has been processed successfully. Is there anything else I can help you with?"
        }

    def process(self, message: str, context: Optional[Dict] = None) -> Dict:
        """
        Process a user message in the context of an order.

        Args:
            message: The user message to process
            context: The current context of the conversation (optional)

        Returns:
            Dict containing:
                - 'context': Updated context
                - 'response': Agent response
        """
        # Initialize context if not provided
        if context is None:
            context = {'state': 'init'}

        # Get current state
        current_state = context.get('state', 'init')

        # Handle the message based on the current state
        if current_state in self.order_states:
            return self.order_states[current_state](message, context)

        # Default to init state if unknown state
        context['state'] = 'init'
        return self.order_states['init'](message, context)