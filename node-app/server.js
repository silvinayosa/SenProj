const express = require('express');
const path = require('path');
const fs = require('fs');
const cors = require('cors');
const session = require('express-session');
const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());

// Middleware to parse JSON bodies
app.use(express.json());

// Set the view engine to EJS
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views')); // Directory for views

app.use(express.urlencoded({ extended: true }));
// Configure session middleware
app.use(session({
    secret: 'your_secret_key',
    resave: false,
    saveUninitialized: true
  }));

const stripe = require('stripe')('sk_test_51QFDthGl6As4Qq0g27uZTUq1yL4YX2G5wasNDacCFNq7AgH75ELDDkJLmveEarlYn5zAiJV1CqZzxYGdjq3UkNR200No2hbQb5'); // Replace with your Stripe Secret Key

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

app.get('/main-web-page/payment', (req, res) => {
    res.render('main-web-page/payment'); // Renders the payment.ejs file
});

app.post('/create-checkout-session', async (req, res) => {
    // get the price of the product from the front end
    const { price } = req.body;
    const { budget } = req.body;   
 
    const saving = budget - price; // Calculate the saving


    console.log(budget);
    console.log(price);
    console.log(saving);

    const session = await stripe.checkout.sessions.create({
        payment_method_types: ['card'],
        line_items: [
            {
                price_data: {
                    currency: 'usd',
                    product_data: {
                        name: 'Test Product',
                    },
                    unit_amount: price * 100, // Using the price from selected venue
                },
                quantity: 1,
            },
        ],
        mode: 'payment',
        success_url: `${req.headers.origin}/success?price=${saving}&co2Percent=40`, // Pass the price as a query parameter
        cancel_url: `${req.headers.origin}/cancel`,
    });

    res.json({ id: session.id });
}); 

app.get('/main-web-page/success', (req, res) => {
    res.send("/main-web-page/success");
});

app.get('/main-web-page/cancel', (req, res) => {
    res.send("Payment canceled.");
});

// Route for the home page
app.get('/', (req, res) => {
    res.render('index', { s: req.session.user });
  });

app.get('/main-web-page/create-event', (req, res) => {
    res.render('main-web-page/create-event'); // Adjust this if your file structure is different
});

app.get('/main-web-page/prediction', (req, res) => {
    res.render('main-web-page/prediction'); // Adjust this if your file structure is different
});

app.get('/main-web-page/about-us', (req, res) => {
    res.render('main-web-page/about-us'); // Adjust this if your file structure is different
});

app.get('/main-web-page/recomendation-page1', (req, res) => {
    res.render('main-web-page/recomendation-page1'); // Adjust this if your file structure is different
});

app.get('/main-web-page/analysis', (req, res) => {
    res.render('main-web-page/analysis'); // Adjust this if your file structure is different
});

app.get('/main-web-page/analysis2', (req, res) => {
    res.render('main-web-page/analysis2'); // Adjust this if your file structure is different
});

app.get('./node-app/public/js/predictionAPI.js', (req, res) => {
    res.render('./node-app/public/js/predictionAPI.js '); // Adjust this if your file structure is different
});

app.get('/main-web-page/analysis3', (req, res) => {
    res.render('main-web-page/analysis3'); // Adjust this if your file structure is different
});

app.get('/main-web-page/analysis3-2', (req, res) => {
    res.render('main-web-page/analysis3-2'); // Adjust this if your file structure is different
});
app.get('/main-web-page/analysis3-3', (req, res) => {
    res.render('main-web-page/analysis3-3'); // Adjust this if your file structure is different
});

app.get('/main-web-page/kepler', (req, res) => {
    res.render('main-web-page/kepler'); // Adjust this if your file structure is different
});

app.get('/main-web-page/ourteam', (req, res) => {
    res.render('main-web-page/ourteam'); // Adjust this if your file structure is different
});

app.get('/main-web-page/log-in', (req, res) => {
    res.render('main-web-page/log-in'); // Adjust this if your file structure is different
});

app.get('/success', (req, res) => {
    
    res.render('main-web-page/success'); // Adjust this if your file structure is different
});
app.get('/event-list', (req, res) => {
    
    res.render('main-web-page/event-list'); // Adjust this if your file structure is different
});

app.get('/details', (req, res) => {
    
    res.render('main-web-page/details'); // Adjust this if your file structure is different
});

app.get('/details-venues', (req, res) => {
    
    res.render('main-web-page/details-venues'); // Adjust this if your file structure is different
});

app.get('/book-venue', (req, res) => {
    
    res.render('main-web-page/book-venue'); // Adjust this if your file structure is different
});

app.get('/logged', (req, res) => {
    res.render('logged-in-pages/index'); // Adjust this if your file structure is different
});

app.get('/main-web-page/profile', (req, res) => {
    res.render('main-web-page/profile'); // Adjust this if your file structure is different
});

app.post('/main-web-page/log-in', (req, res) => {
    req.session.user = { username: 's' }; // Simulate a logged-in user
    res.redirect('/');
  });

app.get('/logout', (req, res) => {
    req.session.destroy(err => {
        if (err) {
            return res.redirect('/');
        }
        res.clearCookie('connect.sid');
        res.redirect('/');
    });
});


app.use((req, res, next) => {
    res.setHeader('X-Content-Type-Options', '');  // Remove nosniff
    next();
  });

  
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
