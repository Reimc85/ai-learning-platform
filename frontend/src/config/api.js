// API Configuration
const API_CONFIG = {
  // Determine if we're in development or production
  isDevelopment: import.meta.env.DEV,
  
  // API Base URLs
  development: 'http://localhost:5001/api',
  production: '/api', // Same domain as frontend in production
  
  // Get the appropriate API URL
  getApiUrl() {
    return this.isDevelopment ? this.development : this.production;
  }
};

export const API_BASE_URL = API_CONFIG.getApiUrl();
export default API_CONFIG;

