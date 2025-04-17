from typing import Dict, Optional, Any
from sqlalchemy.orm import Session
from app.database.models import ChatLog, UserInteraction
from app.agents.guard_agent import GuardAgent
from app.agents.classification_agent import ClassificationAgent
from app.agents.order_agent import OrderAgent
from app.agents.details_agent import DetailsAgent
from app.agents.recommendation_agent import RecommendationAgent

class QueryHandler:
    """
    Main handler for processing user queries through the agent pipeline.
    """
    
    def __init__(self, db: Optional[Session] = None, faiss_index=None):
        self.db = db
        
        # Initialize agents
        self.guard_agent = GuardAgent()
        self.classification_agent = ClassificationAgent()
        self.order_agent = OrderAgent(db=self.db)
        self.details_agent = DetailsAgent(db=self.db)
        self.recommendation_agent = RecommendationAgent(db=self.db)
        
        # Store conversation context
        self.contexts = {}
    
    def _log_interaction(self, user_id: int, message: str, intent: str, response: str):
        """
        Log user interaction in the database.
        
        Args:
            user_id: The user ID
            message: The user message
            intent: The classified intent
            response: The agent response
        """
        if not self.db:
            return
        
        try:
            # Log to UserInteraction table
            interaction = UserInteraction(
                user_id=user_id,
                query_text=message,
                intent=intent,
                response=response
            )
            self.db.add(interaction)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(f"Error logging interaction: {e}")
    
    def _log_chat(self, user_id: int, agent_name: str, message: str, response: str):
        """
        Log chat message in the database.
        
        Args:
            user_id: The user ID
            agent_name: The name of the agent that processed the message
            message: The user message
            response: The agent response
        """
        if not self.db:
            return
        
        try:
            # Log to ChatLog table
            chat_log = ChatLog(
                user_id=user_id,
                agent_name=agent_name,
                message=message,
                response=response
            )
            self.db.add(chat_log)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(f"Error logging chat: {e}")
    
    def process_query(self, message: str, user_id: Optional[int] = None, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a user query through the agent pipeline.

        Args:
            message: The user message
            user_id: The user ID (optional)
            session_id: The session ID for maintaining context (optional)
            
        Returns:
            Dict containing the response and additional information
        """
        print(f"\n[QueryHandler] Processing message: '{message}'")
        
        try:
            # Use a default user ID if not provided
            if user_id is None:
                user_id = 1  # Anonymous user

            # Use message as session ID if not provided
            if session_id is None:
                session_id = str(user_id)

            # Initialize result dictionary
            result = {
                'status': 'success',
                'message': message,
                'response': '',
                'intent': 'unknown',
                'agent': 'details_agent',  # Default to details agent
                'additional_data': {}
            }
            
            # Step 1: Guard Agent - Filter inappropriate content
            guard_result = self.guard_agent.process(message)

            if guard_result['status'] == 'rejected':
                result['status'] = 'rejected'
                result['response'] = guard_result['message']
                result['agent'] = 'guard_agent'
                
                # Log the rejected interaction
                try:
                    self._log_chat(user_id, 'guard_agent', message, guard_result['message'])
                except Exception as e:
                    print(f"Error logging rejected message: {e}")
                
                return result

            # Get the filtered message
            filtered_message = guard_result['filtered_message']

            # Step 2: Classification Agent - Determine intent
            classification_result = self.classification_agent.process(filtered_message)

            intent = classification_result['intent']
            agent_name = classification_result['agent']

            result['intent'] = intent
            result['agent'] = agent_name

            # Step 3: Route to appropriate agent based on intent
            try:
                # For simplicity, we'll just use the Details Agent for now
                details_result = self.details_agent.process(filtered_message)
                
                # Set response
                result['response'] = details_result['response']
                result['additional_data'] = {
                    'products': details_result['products'],
                    'faqs': details_result['faqs']
                }
                
                # Log the interaction
                try:
                    self._log_interaction(user_id, message, intent, result['response'])
                    self._log_chat(user_id, 'details_agent', message, result['response'])
                except Exception as e:
                    print(f"Error logging interaction: {e}")
                
                return result
                
            except Exception as e:
                print(f"Error in agent processing: {e}")
                result['status'] = 'error'
                result['response'] = "I'm sorry, but I encountered an error while processing your request. Please try again."
                return result
                
        except Exception as e:
            print(f"Unhandled error: {e}")
            return {
                'status': 'error',
                'message': message,
                'response': "I'm sorry, but I encountered an unexpected error. Please try again later.",
                'intent': 'error',
                'agent': 'error',
                'additional_data': {}
            }
