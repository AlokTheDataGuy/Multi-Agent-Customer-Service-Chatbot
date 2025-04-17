import React, { useState, useEffect } from 'react';
import Header from '../components/Header.jsx';
import OrderCard from '../components/OrderCard.jsx';
import { getOrders } from '../services/api.js';

const Orders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Mock user ID for development
  const userId = 1;

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        setLoading(true);
        const data = await getOrders(userId);
        setOrders(data);
        setError(null);
      } catch (err) {
        setError('Failed to fetch orders. Please try again later.');
        console.error(err);
        
        // Mock data for development
        setOrders([
          {
            order_id: 12345,
            user_id: 1,
            order_status: 'Pending',
            products: [
              { name: 'Wireless Headphones', quantity: 1, price: 79.99 },
              { name: 'Smart Watch', quantity: 1, price: 149.99 }
            ],
            total_price: 229.98,
            payment_status: 'Paid',
            shipping_address: '123 Main St, Anytown, USA',
            created_at: '2023-03-15T10:30:00Z'
          },
          {
            order_id: 12346,
            user_id: 1,
            order_status: 'Completed',
            products: [
              { name: 'Coffee Maker', quantity: 1, price: 89.99 }
            ],
            total_price: 89.99,
            payment_status: 'Paid',
            shipping_address: '123 Main St, Anytown, USA',
            created_at: '2023-03-10T14:45:00Z'
          }
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, [userId]);

  return (
    <div>
      <Header />
      <div className="container orders-container">
        <h1>Your Orders</h1>
        
        {loading ? (
          <p>Loading orders...</p>
        ) : error ? (
          <p style={{ color: 'red' }}>{error}</p>
        ) : (
          <div>
            {orders.length > 0 ? (
              orders.map(order => (
                <OrderCard key={order.order_id} order={order} />
              ))
            ) : (
              <p>You don't have any orders yet.</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Orders;
