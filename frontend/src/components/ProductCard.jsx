import React from 'react';

const ProductCard = ({ product }) => {
  return (
    <div className="product-card">
      <img 
        src={product.image_url || 'https://via.placeholder.com/300x200?text=Product+Image'} 
        alt={product.name} 
        className="product-image" 
      />
      <div className="product-info">
        <h3 className="product-name">{product.name}</h3>
        <p className="product-price">${product.price.toFixed(2)}</p>
        <p className="product-description">
          {product.description.length > 100 
            ? `${product.description.substring(0, 100)}...` 
            : product.description}
        </p>
        <button className="product-button">Add to Cart</button>
      </div>
    </div>
  );
};

export default ProductCard;
