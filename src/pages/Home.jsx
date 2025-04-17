import { Link } from 'react-router-dom';
import Header from '../components/Header';

const Home = () => {
  return (
    <div>
      <Header />
      <div className="container">
        <div style={{ padding: '50px 0', textAlign: 'center' }}>
          <h1 style={{ fontSize: '2.5rem', marginBottom: '20px' }}>Welcome to E-Commerce Chatbot</h1>
          <p style={{ fontSize: '1.2rem', marginBottom: '30px', maxWidth: '800px', margin: '0 auto 30px' }}>
            Your AI-powered shopping assistant that helps you find products, place orders, and get answers to your questions.
          </p>
          
          <div style={{ display: 'flex', justifyContent: 'center', gap: '20px', flexWrap: 'wrap' }}>
            <Link to="/chat" style={{ 
              padding: '15px 30px', 
              backgroundColor: '#4a90e2', 
              color: 'white', 
              borderRadius: '5px', 
              textDecoration: 'none',
              fontSize: '1.1rem',
              fontWeight: '500'
            }}>
              Start Chatting
            </Link>
            
            <Link to="/products" style={{ 
              padding: '15px 30px', 
              backgroundColor: '#50b7f5', 
              color: 'white', 
              borderRadius: '5px', 
              textDecoration: 'none',
              fontSize: '1.1rem',
              fontWeight: '500'
            }}>
              Browse Products
            </Link>
          </div>
        </div>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '30px', margin: '50px 0' }}>
          <div style={{ backgroundColor: 'white', padding: '30px', borderRadius: '8px', boxShadow: '0 2px 5px rgba(0,0,0,0.1)' }}>
            <h2 style={{ marginBottom: '15px', color: '#4a90e2' }}>Smart Recommendations</h2>
            <p>Get personalized product recommendations based on your preferences and shopping history.</p>
          </div>
          
          <div style={{ backgroundColor: 'white', padding: '30px', borderRadius: '8px', boxShadow: '0 2px 5px rgba(0,0,0,0.1)' }}>
            <h2 style={{ marginBottom: '15px', color: '#4a90e2' }}>Easy Ordering</h2>
            <p>Place orders through a simple conversation with our AI assistant. No complicated forms to fill out.</p>
          </div>
          
          <div style={{ backgroundColor: 'white', padding: '30px', borderRadius: '8px', boxShadow: '0 2px 5px rgba(0,0,0,0.1)' }}>
            <h2 style={{ marginBottom: '15px', color: '#4a90e2' }}>Instant Answers</h2>
            <p>Get immediate answers to your questions about products, shipping, returns, and more.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
