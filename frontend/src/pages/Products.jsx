import React, { useState, useEffect } from 'react';
import Header from '../components/Header.jsx';
import ProductCard from '../components/ProductCard.jsx';
import { getProducts } from '../services/api.js';

const Products = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState('');
  
  const categories = [
    'All Categories',
    'Electronics',
    'Clothing',
    'Home & Kitchen',
    'Books',
    'Toys',
    'Beauty',
    'Sports'
  ];

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        const category = selectedCategory === 'All Categories' ? '' : selectedCategory;
        const data = await getProducts(category);
        setProducts(data);
        setError(null);
      } catch (err) {
        setError('Failed to fetch products. Please try again later.');
        console.error(err);
        
        // Mock data for development
        setProducts([
          {
            product_id: 1,
            name: 'Wireless Headphones',
            category: 'Electronics',
            price: 79.99,
            stock: 45,
            description: 'High-quality wireless headphones with noise cancellation and 20-hour battery life.',
            image_url: 'https://via.placeholder.com/300x200?text=Headphones'
          },
          {
            product_id: 2,
            name: 'Cotton T-Shirt',
            category: 'Clothing',
            price: 19.99,
            stock: 100,
            description: 'Comfortable 100% cotton t-shirt available in multiple colors.',
            image_url: 'https://via.placeholder.com/300x200?text=T-Shirt'
          },
          {
            product_id: 3,
            name: 'Smart Watch',
            category: 'Electronics',
            price: 149.99,
            stock: 30,
            description: 'Feature-packed smartwatch with heart rate monitor, GPS, and 5-day battery life.',
            image_url: 'https://via.placeholder.com/300x200?text=Smart+Watch'
          },
          {
            product_id: 4,
            name: 'Coffee Maker',
            category: 'Home & Kitchen',
            price: 89.99,
            stock: 25,
            description: 'Programmable coffee maker with 12-cup capacity and built-in grinder.',
            image_url: 'https://via.placeholder.com/300x200?text=Coffee+Maker'
          }
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, [selectedCategory]);

  const handleCategoryChange = (e) => {
    setSelectedCategory(e.target.value);
  };

  return (
    <div>
      <Header />
      <div className="container products-container">
        <h1>Products</h1>
        
        <div style={{ marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <label htmlFor="category-select" style={{ marginRight: '10px' }}>Filter by Category:</label>
            <select 
              id="category-select" 
              value={selectedCategory} 
              onChange={handleCategoryChange}
              style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
            >
              <option value="">All Categories</option>
              {categories.map((category, index) => (
                <option key={index} value={category}>{category}</option>
              ))}
            </select>
          </div>
          
          <div>
            <input 
              type="text" 
              placeholder="Search products..." 
              style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ccc', width: '250px' }}
            />
          </div>
        </div>
        
        {loading ? (
          <p>Loading products...</p>
        ) : error ? (
          <p style={{ color: 'red' }}>{error}</p>
        ) : (
          <div className="products-grid">
            {products.length > 0 ? (
              products.map(product => (
                <ProductCard key={product.product_id} product={product} />
              ))
            ) : (
              <p>No products found. Try a different category.</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Products;
