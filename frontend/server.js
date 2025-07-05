const express = require('express');
const path = require('path');
const fs = require('fs');
const app = express();
const port = process.env.PORT || 8080;

// Correctly define the absolute path to the build directory
// __dirname is the directory where server.js resides (/app/frontend)
const buildPath = path.join(__dirname, 'build');
const indexPath = path.join(buildPath, 'index.html');

console.log(`Serving static files from: ${buildPath}`);
console.log(`Attempting to serve index.html from: ${indexPath}`);

if (!fs.existsSync(buildPath)) {
    console.error(`ERROR: Build directory does not exist at ${buildPath}`);
} else if (!fs.lstatSync(buildPath).isDirectory()) {
    console.error(`ERROR: Build path ${buildPath} is not a directory`);
} else {
    console.log(`Build directory ${buildPath} exists and is a directory.`);
}

if (!fs.existsSync(indexPath)) {
    console.error(`ERROR: index.html does not exist at ${indexPath}`);
} else {
    console.log(`index.html found at ${indexPath}.`);
}

app.use(express.static(buildPath));

app.get('*', (req, res) => {
  console.log(`Request for: ${req.url}, serving fallback index.html`);
  res.sendFile(indexPath, (err) => {
    if (err) {
      console.error(`Error sending index.html for ${req.url}:`, err);
      res.status(500).send('Internal Server Error during fallback');
    }
  });
});

app.listen(port, () => {
  console.log(`Frontend server listening on port ${port}`);
});
