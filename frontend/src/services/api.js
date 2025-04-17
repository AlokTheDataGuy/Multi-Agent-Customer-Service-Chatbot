import axios from 'axios';

// Create axios instance with base URL
const api = axios.create({
  baseURL: import.meta.env.PROD ? '/api' : 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: false
});

// Add request interceptor for debugging
api.interceptors.request.use(request => {
  console.log('Starting API Request:', request);
  return request;
});

// Add response interceptor for debugging
api.interceptors.response.use(
  response => {
    console.log('API Response:', response);
    return response;
  },
  error => {
    console.error('API Error Response:', error.response || error);
    return Promise.reject(error);
  }
);

// Chat API
export const sendChatMessage = async (message, userId = null, sessionId = null) => {
  try {
    const response = await api.post('/chat/', {
      message,
      user_id: userId,
      session_id: sessionId,
    });
    return response.data;
  } catch (error) {
    console.error('Error sending chat message:', error);
    throw error;
  }
};

// Products API
export const getProducts = async (category = null) => {
  try {
    const params = category ? { category } : {};
    const response = await api.get('/products/', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching products:', error);
    throw error;
  }
};

export const getProductById = async (productId) => {
  try {
    const response = await api.get(`/products/${productId}/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching product ${productId}:`, error);
    throw error;
  }
};

// Orders API
export const getOrders = async (userId) => {
  try {
    const response = await api.get('/orders/', {
      params: { user_id: userId },
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching orders:', error);
    throw error;
  }
};

export const createOrder = async (orderData) => {
  try {
    const response = await api.post('/orders/', orderData);
    return response.data;
  } catch (error) {
    console.error('Error creating order:', error);
    throw error;
  }
};

// FAQ API
export const getFaqs = async () => {
  try {
    const response = await api.get('/faq/');
    return response.data;
  } catch (error) {
    console.error('Error fetching FAQs:', error);
    throw error;
  }
};

export default api;
