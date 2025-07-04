const express = require('express');
const path = require('path');
const app = express();
const port = process.env.PORT || 8080; // Use Railway's PORT env var or default to 8080

// Serve static files from the 'build' directory
app.use(express.static(path.join(__dirname, 'build')));

// Handle all other routes by serving index.html (SPA fallback)
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

app.listen(port, () => {
  console.log(`Frontend server listening on port ${port}`);
});
