import React, { useRef, useEffect } from 'react';
import PropTypes from 'prop-types';
import MessageItem from './MessageItem';
import '../styles/MessageList.css';

const MessageList = ({ messages, isLoading }) => {
  const messagesEndRef = useRef(null);

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="message-list">
      {messages.map((message, index) => (
        <MessageItem
          key={index}
          message={message.text}
          isUser={message.isUser}
          hasImage={message.hasImage}
          imageUrl={message.imageUrl}
        />
      ))}
      
      {isLoading && (
        <div className="message-item assistant">
          <div className="avatar">
            <span>🤖</span>
          </div>
          <div className="message-bubble">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      )}
      
      <div ref={messagesEndRef} />
    </div>
  );
};

MessageList.propTypes = {
  messages: PropTypes.arrayOf(
    PropTypes.shape({
      text: PropTypes.string.isRequired,
      isUser: PropTypes.bool.isRequired,
      hasImage: PropTypes.bool,
      imageUrl: PropTypes.string
    })
  ).isRequired,
  isLoading: PropTypes.bool
};

MessageList.defaultProps = {
  isLoading: false
};

export default MessageList;
