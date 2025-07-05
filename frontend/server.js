const express = require('express');
const path = require('path');
const app = express();
const port = process.env.PORT || 8080;

// Define the absolute path to the build directory
// process.cwd() should be /app/frontend in the Railway container
const buildPath = path.join(process.cwd(), 'build');

console.log(`Serving static files from: ${buildPath}`); // Add this for debugging

// Serve static files from the 'build' directory
app.use(express.static(buildPath));

// Handle all other routes by serving index.html (SPA fallback)
app.get('*', (req, res) => {
  console.log(`Request for: ${req.url}, serving fallback index.html`); // Add this for debugging
  res.sendFile(path.join(buildPath, 'index.html'));
});

app.listen(port, () => {
  console.log(`Frontend server listening on port ${port}`);
});
