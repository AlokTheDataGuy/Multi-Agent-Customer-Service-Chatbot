import React from 'react';

const OrderCard = ({ order }) => {
  // Function to get status class
  const getStatusClass = (status) => {
    switch (status.toLowerCase()) {
      case 'pending':
        return 'pending';
      case 'completed':
        return 'completed';
      case 'cancelled':
        return 'cancelled';
      default:
        return '';
    }
  };

  return (
    <div className="order-card">
      <div className="order-header">
        <div className="order-id">Order #{order.order_id}</div>
        <div className={`order-status ${getStatusClass(order.order_status)}`}>
          {order.order_status}
        </div>
      </div>
      
      <div className="order-items">
        {Array.isArray(order.products) ? (
          order.products.map((item, index) => (
            <div key={index} className="order-item">
              <div className="order-item-name">
                {item.name} x {item.quantity}
              </div>
              <div className="order-item-price">
                ${(item.price * item.quantity).toFixed(2)}
              </div>
            </div>
          ))
        ) : (
          <div className="order-item">
            <div className="order-item-name">
              Product ID: {order.products.product_id} x {order.products.quantity}
            </div>
          </div>
        )}
      </div>
      
      <div className="order-total">
        <div>Total</div>
        <div>${order.total_price.toFixed(2)}</div>
      </div>
    </div>
  );
};

export default OrderCard;
