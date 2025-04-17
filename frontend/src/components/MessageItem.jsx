import React, { useState } from 'react';
import PropTypes from 'prop-types';
import ImageDisplay from './ImageDisplay';
import '../styles/MessageItem.css';

const MessageItem = ({ message, isUser, hasImage, imageUrl }) => {
  const [showImageModal, setShowImageModal] = useState(false);

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
    <div className={`message-item ${isUser ? 'user' : 'assistant'}`}>
      <div className="avatar">
        <span>{isUser ? '👤' : '🤖'}</span>
      </div>
      <div className="message-bubble">
        <div 
          className="message-content"
          dangerouslySetInnerHTML={{ __html: formatMessage(message) }}
        />
        
        {hasImage && imageUrl && (
          <div className="message-image">
            <img 
              src={imageUrl} 
              alt="Shared image" 
              onClick={() => setShowImageModal(true)}
            />
          </div>
        )}
      </div>
      
      {hasImage && imageUrl && showImageModal && (
        <ImageDisplay 
          imageUrl={imageUrl} 
          onClose={() => setShowImageModal(false)} 
        />
      )}
    </div>
  );
};

MessageItem.propTypes = {
  message: PropTypes.string.isRequired,
  isUser: PropTypes.bool.isRequired,
  hasImage: PropTypes.bool,
  imageUrl: PropTypes.string
};

MessageItem.defaultProps = {
  hasImage: false,
  imageUrl: ''
};

export default MessageItem;
