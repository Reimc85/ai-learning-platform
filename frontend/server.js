const express = require('express');
const path = require('path');
const fs = require('fs');
const app = express();
const port = process.env.PORT || 8080;

// __dirname will now correctly point to /app/frontend
const buildPath = path.join(__dirname, 'build');
const indexPath = path.join(buildPath, 'index.html');

console.log(`Serving static files from: ${buildPath}`);
console.log(`Attempting to serve index.html from: ${indexPath}`);

if (!fs.existsSync(buildPath)) {
    console.error(`ERROR: Build directory does not exist at ${buildPath}`);
    process.exit(1);
} else if (!fs.lstatSync(buildPath).isDirectory()) {
    console.error(`ERROR: Build path ${buildPath} is not a directory`);
    process.exit(1);
} else {
    console.log(`Build directory ${buildPath} exists and is a directory.`);
}

if (!fs.existsSync(indexPath)) {
    console.error(`ERROR: index.html does not exist at ${indexPath}`);
    process.exit(1);
} else {
    console.log(`index.html found at ${indexPath}.`);
}

// Serve static files from the build directory
// This middleware will try to find a matching file for the request.
// If it finds one (e.g., /static/js/main.js), it serves it.
// If it doesn't find one, it passes the request to the next middleware.
app.use(express.static(buildPath));

// This catch-all route must come AFTER express.static
// It will handle any request that wasn't handled by express.static
// and serve the index.html for SPA routing.
app.get('*', (req, res) => {
  console.log(`Request for: ${req.url}, serving fallback index.html`);
  res.sendFile(indexPath, (err) => {
    if (err) {
      console.error(`Error sending index.html for ${req.url}:`, err);
      // If index.html itself cannot be sent, respond with a server error
      res.status(500).send('Internal Server Error during fallback');
    }
  });
});

app.listen(port, () => {
  console.log(`Frontend server listening on port ${port}`);
});
