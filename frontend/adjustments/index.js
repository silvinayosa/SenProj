import React from 'react';
import PricingCard from '../components/PricingCard';
import styles from '../styles/Home.module.css';


const HomePage = () => {
  const pricingPlans = [
    {
      title: 'Small Party',
      price: '350',
      description: 'Typically for birthday parties and small gatherings.',
      features: ['0-50 Guests', 'Non-alcoholic beverages', 'Snacks']
    },
    {
      title: 'Medium Party',
      price: '750',
      description: 'Typically for weddings, fundraising, or family reunions.',
      features: ['50-100 Guests','Non-alcoholic beverages', 'Snacks']
    },
    {
      title: 'Large Party',
      price: '1050',
      description: 'Typically for big concerts and gatherings.',
      features: ['100-200 Guests', 'Non-alcoholic beverages', 'Snacks']
    },
  ];

  return (
    <div className="pricing-container">
      {pricingPlans.map((plan, index) => (
        <PricingCard key={index} {...plan} />
      ))}
    </div>
  );
};

export default HomePage;
