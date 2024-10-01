const express = require('express');
const path = require('path');
const browserSync = require('browser-sync');

const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files from the 'connect' directory
app.use(express.static(path.join(__dirname, 'connect')));

// Serve HTML files from the 'connect' directory and its subdirectories
app.get('*', (req, res) => {
    const filePath = path.join(__dirname, 'connect', req.path);

    // Ensure the requested path has an .html extension
    let finalPath = filePath.endsWith('.html') ? filePath : `${filePath}.html`;

    res.sendFile(finalPath, (err) => {
        if (err) {
            // If the file is not found, send a 404 error
            res.status(err.status).send('404: Page Not Found');
        }
    });
});

// Start the server
const server = app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});

// // Integrate BrowserSync
// const bs = browserSync.create();
// bs.init({
//     proxy: `http://localhost:${PORT}`,  // Proxy the Express server
//     files: ['connect/**/*.*'],          // Watch for changes in 'connect' directory
//     port: 3001,                         // Port for BrowserSync (different from Express)
// });

// // Restart BrowserSync when the server restarts
// server.on('listening', () => {
//     console.log('BrowserSync is running on http://localhost:3001');
// });
