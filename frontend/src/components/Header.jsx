import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="header">
      <div className="container header-container">
        <div className="logo">E-Commerce Chatbot</div>
        <ul className="nav-links">
          <li><Link to="/">Home</Link></li>
          <li><Link to="/chat">Chat</Link></li>
          <li><Link to="/products">Products</Link></li>
          <li><Link to="/orders">Orders</Link></li>
        </ul>
      </div>
    </header>
  );
};

export default Header;
