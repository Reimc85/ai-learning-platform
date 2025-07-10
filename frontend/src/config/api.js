// frontend/src/config/api.js

// Get the public domain from Vite's environment variables.
const railwayPublicDomain = import.meta.env.VITE_RAILWAY_PUBLIC_DOMAIN;

// If the VITE_RAILWAY_PUBLIC_DOMAIN is set, use it to construct the production URL.
// Otherwise, fall back to a clean localhost URL for local development.
export const API_BASE_URL = railwayPublicDomain
  ? `https://${railwayPublicDomain}`
  : 'http://localhost:5000'; // The comment has been removed.
