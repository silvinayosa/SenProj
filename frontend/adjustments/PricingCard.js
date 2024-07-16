import React from 'react';
import styles from '../styles/Home.module.css';

const PricingCard = ({ title, price, description, features }) => (
  <div className={styles.card}>
    <h2>{title}</h2>
    <p className={styles.price}>{price} USD</p>
    <p>{description}</p>
    <ul className={styles.featureList}>
      {features.map((feature, index) => (
        <li key={index}>{feature}</li>
      ))}
    </ul>
    <button className={styles.getStartedButton}>Get Started</button>
  </div>
);

export default PricingCard;
