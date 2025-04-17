from typing import Dict, List, Optional
import re

class ClassificationAgent:
    """
    Classification Agent that determines the intent of a user message
    and routes it to the appropriate specialized agent.
    """
    
    def __init__(self):
        # Define patterns for each intent
        self.intent_patterns = {
            'order': [
                r'\b(order|buy|purchase|get|add to cart)\b',
                r'\bhow (can|do) I (order|buy|purchase|get)\b',
                r'\bI want to (order|buy|purchase|get)\b',
                r'\bI would like to (order|buy|purchase|get)\b',
                r'\bId like to (order|buy|purchase|get)\b',
                r'\bcan I (order|buy|purchase|get)\b',
                r'\bplace (an|my) order\b',
                r'\bcheckout\b',
                r'\bshopping cart\b',
                r'\bpayment\b',
            ],
            'details': [
                r'\b(what|tell me about|info|information|details|specs|specifications)\b',
                r'\bhow (does|is|are|can|do)\b',
                r'\bwhat is\b',
                r'\bdescribe\b',
                r'\bfeatures\b',
                r'\bprice\b',
                r'\bcost\b',
                r'\bavailable\b',
                r'\bin stock\b',
                r'\ballerg(y|ies|en)\b',
                r'\bingredients\b',
                r'\bnutrition\b',
                r'\bgluten\b',
                r'\bvegan\b',
                r'\bvegetarian\b',
            ],
            'recommendation': [
                r'\b(recommend|suggestion|suggest|best|popular|top)\b',
                r'\bwhat (should|would) (I|you) (recommend|suggest)\b',
                r'\bcan you (recommend|suggest)\b',
                r'\bsimilar to\b',
                r'\balternative\b',
                r'\blike\b',
                r'\bprefer\b',
            ],
        }
        
        # Compile all patterns for efficiency
        self.compiled_patterns = {}
        for intent, patterns in self.intent_patterns.items():
            self.compiled_patterns[intent] = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    
    def classify_intent(self, message: str) -> str:
        """
        Classify the intent of a user message.
        
        Args:
            message: The user message to classify
            
        Returns:
            The classified intent: 'order', 'details', 'recommendation', or 'unknown'
        """
        # Count matches for each intent
        intent_scores = {intent: 0 for intent in self.intent_patterns.keys()}
        
        for intent, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                if pattern.search(message):
                    intent_scores[intent] += 1
        
        # Find the intent with the highest score
        max_score = 0
        max_intent = 'unknown'
        
        for intent, score in intent_scores.items():
            if score > max_score:
                max_score = score
                max_intent = intent
        
        # If no intent was matched, return 'unknown'
        if max_score == 0:
            return 'unknown'
        
        return max_intent
    
    def process(self, message: str) -> Dict:
        """
        Process a user message and determine which agent should handle it.
        
        Args:
            message: The user message to process
            
        Returns:
            Dict containing:
                - 'intent': The classified intent
                - 'confidence': Confidence score (placeholder for now)
                - 'agent': The agent that should handle the message
        """
        intent = self.classify_intent(message)
        
        # Map intent to agent
        agent_mapping = {
            'order': 'order_agent',
            'details': 'details_agent',
            'recommendation': 'recommendation_agent',
            'unknown': 'details_agent'  # Default to details agent for unknown intents
        }
        
        return {
            'intent': intent,
            'confidence': 1.0,  # Placeholder for now
            'agent': agent_mapping[intent]
        }
