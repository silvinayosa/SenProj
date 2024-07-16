import React from 'react';

const Navbar = () => (
  <nav className="navbar">
    <div className="navbar-container">
      <div className="navbar-logo">
        <a href="#">
          <img src="/path/to/logo.png" alt="Logo" className="logo-img"/>
        </a>
      </div>
      <div className="navbar-links">
        <a href="#">Create Venue</a>
        <a href="#">Prediction</a>
        <a href="#">My Green Venue</a>
        <a href="#"><img src="/path/to/menu-icon.png" alt="Menu" className="menu-icon"/></a>
      </div>
    </div>
    <div className="navbar-categories">
      <a href="#"><img src="/path/to/music-icon.png" alt="Music" className="category-icon"/><span>Music</span></a>
      <a href="#"><img src="/path/to/nightlife-icon.png" alt="Nightlife" className="category-icon"/><span>Nightlife</span></a>
      <a href="#"><img src="/path/to/arts-icon.png" alt="Arts" className="category-icon"/><span>Performing & Visual Arts</span></a>
      <a href="#"><img src="/path/to/holidays-icon.png" alt="Holidays" className="category-icon"/><span>Holidays</span></a>
      <a href="#"><img src="/path/to/health-icon.png" alt="Health" className="category-icon"/><span>Health</span></a>
      <a href="#"><img src="/path/to/hobbies-icon.png" alt="Hobbies" className="category-icon"/><span>Hobbies</span></a>
      <a href="#"><img src="/path/to/business-icon.png" alt="Business" className="category-icon"/><span>Business</span></a>
      <a href="#"><img src="/path/to/food-drinks-icon.png" alt="Food & Drinks" className="category-icon"/><span>Food & Drinks</span></a>
    </div>
  </nav>
);

export default Navbar;
