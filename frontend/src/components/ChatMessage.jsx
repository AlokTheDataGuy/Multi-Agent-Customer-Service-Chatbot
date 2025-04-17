import React from 'react';

const ChatMessage = ({ message, isUser }) => {
  // Function to convert markdown-like formatting to HTML
  const formatMessage = (text) => {
    if (!text) return '';
    
    // Replace ** for bold
    let formattedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Replace newlines with <br>
    formattedText = formattedText.replace(/\n/g, '<br>');
    
    return formattedText;
  };

  return (
    <div className={`message ${isUser ? 'user' : 'bot'}`}>
      <div className="message-content">
        <div dangerouslySetInnerHTML={{ __html: formatMessage(message) }} />
      </div>
    </div>
  );
};

export default ChatMessage;
