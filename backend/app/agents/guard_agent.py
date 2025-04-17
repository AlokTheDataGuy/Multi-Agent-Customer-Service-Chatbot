import re
from typing import Dict, List, Tuple, Optional

class GuardAgent:
    """
    Guard Agent that filters out inappropriate or irrelevant messages
    before they are processed by other agents.
    """

    def __init__(self):
        # Patterns for detecting inappropriate content
        self.profanity_patterns = [
            r'\b(fuck|shit|ass|bitch|cunt|damn|dick|piss|cock|pussy|asshole)\b',
            # Add more patterns as needed
        ]

        # Patterns for detecting spam or irrelevant content
        self.spam_patterns = [
            r'buy now',
            r'click here',
            r'limited time offer',
            r'www\.',
            r'http',
            # Add more patterns as needed
        ]

        # Compile all patterns for efficiency
        self.compiled_profanity = [re.compile(pattern, re.IGNORECASE) for pattern in self.profanity_patterns]
        self.compiled_spam = [re.compile(pattern, re.IGNORECASE) for pattern in self.spam_patterns]

    def check_message(self, message: str) -> Tuple[bool, Optional[str]]:
        """
        Check if a message contains inappropriate or irrelevant content.

        Args:
            message: The user message to check

        Returns:
            Tuple containing:
                - Boolean indicating if message is safe (True) or not (False)
                - Optional reason for rejection if message is not safe
        """
        # Check for profanity
        for pattern in self.compiled_profanity:
            if pattern.search(message):
                return False, "Your message contains inappropriate language. Please rephrase your request."

        # Check for spam or irrelevant content
        for pattern in self.compiled_spam:
            if pattern.search(message):
                return False, "Your message appears to be spam or promotional content, which is not supported."

        # Check for empty or too short messages
        if not message.strip() or len(message.strip()) < 2:
            return False, "Please provide a valid message."

        # Check for extremely long messages
        if len(message) > 500:
            return False, "Your message is too long. Please keep your message under 500 characters."

        return True, None

    def process(self, message: str) -> Dict:
        """
        Process a user message and determine if it should be passed to the next agent.

        Args:
            message: The user message to process

        Returns:
            Dict containing:
                - 'status': 'success' or 'rejected'
                - 'message': Original message if successful, or rejection reason if rejected
                - 'filtered_message': Cleaned message if successful, None if rejected
        """
        is_safe, reason = self.check_message(message)

        if is_safe:
            # Message is safe, return cleaned message
            return {
                'status': 'success',
                'message': message,
                'filtered_message': message.strip()
            }
        else:
            # Message is not safe, return rejection reason
            return {
                'status': 'rejected',
                'message': reason,
                'filtered_message': None
            }