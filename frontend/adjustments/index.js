import React from 'react';
import ContactForm from '../components/ContactForm';

const Home = () => (
  <>
    <div className="contact-hero-section">
      <div className="container">
        <div className="text-content">
          <h1 className="contact-heading">Get in touch today to schedule your Event.</h1>
          <p className="sub-heading">
            Just fill out this short form to get started in your life-changing journey. If you prefer, you can contact us below directly.
          </p>
          <div className="contact-info">
            <p>Email: silvseniorproject25@gmail.com</p>
            <p>Phone: +886958442291</p>
          </div>
        </div>
        <div className="form-wrapper">
          <ContactForm />
        </div>
      </div>
    </div>
    <div className="stats-bar">
      <div className="stat">
        <div className="stat-number">400</div>
        <div className="stat-description">Total Users</div>
      </div>
      <div className="stat">
        <div className="stat-number">57%</div>
        <div className="stat-description">Current CO2 Emission</div>
      </div>
      <div className="stat">
        <div className="stat-number">10</div>
        <div className="stat-description">Total Cities Covered</div>
      </div>
      <div className="stat">
        <div className="stat-number">97.98%</div>
        <div className="stat-description">Prediction Accuracy</div>
      </div>
    </div>
  </>
);

export default Home;
