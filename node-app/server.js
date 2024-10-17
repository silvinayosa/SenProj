const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Set the view engine to EJS
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views')); // Directory for views

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Route for the home page
app.get('/', (req, res) => {
    res.render('index'); // Renders views/index.ejs
});

app.get('/main-web-page/create-event', (req, res) => {
    res.render('main-web-page/create-event'); // Adjust this if your file structure is different
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
