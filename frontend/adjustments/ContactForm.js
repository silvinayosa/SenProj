import React, { useState } from 'react';

const ContactForm = () => {
  const [eventType, setEventType] = useState('');

  const eventTypes = ["Parties", "Convention", "Fundraisers", "Seminars", "Weddings", "Corporate Events"];

  return (
    <form className="contact-form">
      <div className="form-group">
        <label htmlFor="eventName">Event Name</label>
        <input type="text" id="eventName" name="eventName" />
      </div>
      <div className="form-group">
        <label htmlFor="numberOfGuests">No. of Guests</label>
        <input type="number" id="numberOfGuests" name="numberOfGuests" />
      </div>
      <div className="form-group">
        <label>Type of Event</label>
        <div className="event-type-buttons">
          {eventTypes.map(type => (
            <button
              key={type}
              type="button"
              className={`event-button ${eventType === type ? 'active' : ''}`}
              onClick={() => setEventType(type)}
            >
              {type}
            </button>
          ))}
        </div>
      </div>
      <div className="form-group">
        <label htmlFor="date">Date</label>
        <input type="date" id="date" name="date" />
      </div>
      <div className="form-group">
        <label htmlFor="email">Email</label>
        <input type="email" id="email" name="email" />
      </div>
      <div className="form-group">
        <label htmlFor="description">Describe Your Event</label>
        <textarea id="description" name="description"></textarea>
      </div>
      <button type="submit">Next</button>
    </form>
  );
};

export default ContactForm;
