const express = require('express');
const path = require('path');
const fs = require('fs'); // Import file system module
const app = express();
const port = process.env.PORT || 8080;

const buildPath = path.join(process.cwd(), 'build');
const indexPath = path.join(buildPath, 'index.html'); // Path to index.html

console.log(`Serving static files from: ${buildPath}`);
console.log(`Attempting to serve index.html from: ${indexPath}`); // Log index.html path

// Check if buildPath exists and is a directory
if (!fs.existsSync(buildPath)) {
    console.error(`ERROR: Build directory does not exist at ${buildPath}`);
    // You might want to exit or throw an error here in production
} else if (!fs.lstatSync(buildPath).isDirectory()) {
    console.error(`ERROR: Build path ${buildPath} is not a directory`);
} else {
    console.log(`Build directory ${buildPath} exists and is a directory.`);
}

// Check if index.html exists
if (!fs.existsSync(indexPath)) {
    console.error(`ERROR: index.html does not exist at ${indexPath}`);
} else {
    console.log(`index.html found at ${indexPath}.`);
}


app.use(express.static(buildPath));

app.get('*', (req, res) => {
  console.log(`Request for: ${req.url}, serving fallback index.html`);
  // Ensure we are sending the file from the correct absolute path
  res.sendFile(indexPath, (err) => { // Use indexPath directly
    if (err) {
      console.error(`Error sending index.html for ${req.url}:`, err);
      res.status(500).send('Internal Server Error during fallback');
    }
  });
});

app.listen(port, () => {
  console.log(`Frontend server listening on port ${port}`);
});
