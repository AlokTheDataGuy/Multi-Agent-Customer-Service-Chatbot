import { useState, useEffect } from 'react'
import './styles/App.css'
import { sendChatMessage } from './services/api'
import MessageList from './components/MessageList'
import ChatInterface from './components/ChatInterface'
import ImageUpload from './components/ImageUpload'

function App() {
  const [messages, setMessages] = useState([
    { text: 'Hello! I\'m your e-commerce assistant. How can I help you today?', isUser: false }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [uploadedImage, setUploadedImage] = useState(null);

  // Generate a session ID when the component mounts
  useEffect(() => {
    setSessionId(`session_${Date.now()}`);
  }, []);

  const handleSendMessage = async (message) => {
    if (!message.trim()) return;

    // Add user message to chat
    const userMessage = {
      text: message,
      isUser: true,
      hasImage: !!uploadedImage,
      imageUrl: uploadedImage ? URL.createObjectURL(uploadedImage) : null
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    // Reset uploaded image after sending
    setUploadedImage(null);

    try {
      console.log('Sending message to API:', message);

      // Send message to API
      // TODO: Add image upload functionality to the API
      const response = await sendChatMessage(message, null, sessionId);
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

  const handleImageUpload = (file) => {
    setUploadedImage(file);
  };

  return (
    <div className="app-container">
      <header className="chat-header">
        <h1>E-Commerce Assistant</h1>
        <p>Ask me about products, orders, or get recommendations</p>
      </header>

      <div className="chat-main">
        <MessageList
          messages={messages}
          isLoading={isLoading}
        />

        {uploadedImage && (
          <div style={{ padding: '0 var(--spacing-md)' }}>
            <ImageUpload onImageUpload={handleImageUpload} />
          </div>
        )}

        <ChatInterface
          onSendMessage={handleSendMessage}
          isLoading={isLoading}
        />
      </div>
    </div>
  )
}

export default App
