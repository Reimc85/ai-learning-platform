// frontend/src/config/api.js

// Get the public domain from Vite's environment variables, which are injected at build time.
const railwayPublicDomain = import.meta.env.VITE_RAILWAY_PUBLIC_DOMAIN;

// Check if the railwayPublicDomain variable exists.
// If it does, construct the production URL by PREPENDING "https://".
// This is the crucial fix.
// If it doesn't exist (e.g., in local development ), fall back to the local server URL.
export const API_BASE_URL = railwayPublicDomain
  ? `https://${railwayPublicDomain}`
  : 'http://localhost:5000';


