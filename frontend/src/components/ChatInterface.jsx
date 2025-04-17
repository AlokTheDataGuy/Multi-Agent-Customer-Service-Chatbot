import React, { useState } from 'react';
import PropTypes from 'prop-types';
import '../styles/ChatInterface.css';

const ChatInterface = ({ onSendMessage, isLoading }) => {
  const [message, setMessage] = useState('');
  const [showFileUpload, setShowFileUpload] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim()) {
      onSendMessage(message);
      setMessage('');
    }
  };

  const handleFileUpload = () => {
    setShowFileUpload(!showFileUpload);
    // Implement file upload functionality here
  };

  return (
    <div className="chat-interface">
      {showFileUpload && (
        <div className="file-upload-container">
          <input type="file" accept="image/*" className="file-input" />
          <button
            className="cancel-upload-btn"
            onClick={() => setShowFileUpload(false)}
          >
            Cancel
          </button>
        </div>
      )}
      <form onSubmit={handleSubmit} className="message-form">
        <button
          type="button"
          className="upload-btn"
          onClick={handleFileUpload}
          aria-label="Upload file"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="17 8 12 3 7 8"></polyline>
            <line x1="12" y1="3" x2="12" y2="15"></line>
          </svg>
        </button>
        <div style={{ flex: 1, minWidth: 0 }}>
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type a message..."
            disabled={isLoading}
            className="message-input"
          />
        </div>
        <button
          type="submit"
          className="send-btn"
          disabled={!message.trim() || isLoading}
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        </button>
      </form>
    </div>
  );
};

ChatInterface.propTypes = {
  onSendMessage: PropTypes.func.isRequired,
  isLoading: PropTypes.bool
};

ChatInterface.defaultProps = {
  isLoading: false
};

export default ChatInterface;
