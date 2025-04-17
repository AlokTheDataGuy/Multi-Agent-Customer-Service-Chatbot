import React, { useState, useEffect, useRef } from 'react';
import Header from '../components/Header.jsx';
import ChatMessage from '../components/ChatMessage.jsx';
import { sendChatMessage } from '../services/api.js';

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
      console.log('Sending message to API:', input);

      // Send message to API
      const response = await sendChatMessage(input, null, sessionId);
      console.log('API response received:', response);

      // Add bot response to chat
      if (response && response.response) {
        const botMessage = { text: response.response, isUser: false };
        setMessages(prev => [...prev, botMessage]);

        // If there are product recommendations, display them
        if (response.additional_data && response.additional_data.products && response.additional_data.products.length > 0) {
          console.log('Products:', response.additional_data.products);

          // Add product recommendations as a message
          const products = response.additional_data.products;
          const productMessage = {
            text: `Here are some products that might interest you:\n${products.map((p, i) => `${i+1}. **${p.name}** - $${p.price.toFixed(2)}`).join('\n')}`,
            isUser: false
          };
          setMessages(prev => [...prev, productMessage]);
        }
      } else {
        console.error('Invalid response format:', response);
        const errorMessage = {
          text: 'Received an invalid response from the server. Please try again.',
          isUser: false
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      console.error('Error sending message:', error);

      // Get detailed error information
      let errorText = 'Sorry, there was an error processing your request. Please try again.';

      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.error('Error response data:', error.response.data);
        console.error('Error response status:', error.response.status);
        console.error('Error response headers:', error.response.headers);

        if (error.response.data && error.response.data.detail) {
          errorText = `Error: ${error.response.data.detail}`;
        }
      } else if (error.request) {
        // The request was made but no response was received
        console.error('Error request:', error.request);
        errorText = 'No response received from the server. Please check your connection.';
      } else {
        // Something happened in setting up the request that triggered an Error
        console.error('Error message:', error.message);
        errorText = `Error: ${error.message}`;
      }

      // Add error message to chat
      const errorMessage = {
        text: errorText,
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
