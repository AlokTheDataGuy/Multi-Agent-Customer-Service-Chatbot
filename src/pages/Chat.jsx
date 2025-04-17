import { useState, useEffect, useRef } from 'react';
import Header from '../components/Header';
import ChatMessage from '../components/ChatMessage';
import { sendChatMessage } from '../services/api';

const Chat = () => {
  const [messages, setMessages] = useState([
    { text: 'Hello! How can I help you today?', isUser: false }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  // Generate a session ID when the component mounts
  useEffect(() => {
    setSessionId(`session_${Date.now()}`);
  }, []);

  // Scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!input.trim()) return;
    
    // Add user message to chat
    const userMessage = { text: input, isUser: true };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    
    try {
      // Send message to API
      const response = await sendChatMessage(input, null, sessionId);
      
      // Add bot response to chat
      const botMessage = { text: response.response, isUser: false };
      setMessages(prev => [...prev, botMessage]);
      
      // If there are product recommendations, display them
      if (response.additional_data && response.additional_data.products && response.additional_data.products.length > 0) {
        // You could display product cards here
        console.log('Products:', response.additional_data.products);
      }
      
    } catch (error) {
      console.error('Error sending message:', error);
      // Add error message to chat
      const errorMessage = { 
        text: 'Sorry, there was an error processing your request. Please try again.', 
        isUser: false 
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <Header />
      <div className="chat-container">
        <div className="chat-main">
          <div className="chat-messages">
            {messages.map((message, index) => (
              <ChatMessage 
                key={index} 
                message={message.text} 
                isUser={message.isUser} 
              />
            ))}
            {isLoading && (
              <div className="message bot">
                <div className="message-content">
                  <p>Typing...</p>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          <form className="chat-input" onSubmit={handleSendMessage}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message here..."
              disabled={isLoading}
            />
            <button type="submit" disabled={isLoading}>
              Send
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Chat;
