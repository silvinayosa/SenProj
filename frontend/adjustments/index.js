// pages/index.js
import Head from 'next/head';

export default function Home() {
  return (
    <>
      <Head>
        <title>Venue Recommendations</title>
      </Head>
      <div className="container">
        <h1 className="title">Venue Recommendations Just For You!</h1>
        <div className="card-container">
          {venues.map((venue, index) => (
            <div key={index} className="card">
              <img src={venue.image} alt={`${venue.name} image`} className="venue-image" />
              <h2 className="venue-name">{venue.name}</h2>
              <p className="venue-location">{`Location: ${venue.location}`}</p>
              <p className="venue-description">{venue.description}</p>
              <div className="price-container">
                <span className="venue-price">{`From £${venue.price}/night`}</span>
                <span className="venue-discount">{`${venue.discount} OFF`}</span>
              </div>
              <div className="features">
                {venue.features.map(feature => (
                  <span key={feature} className="feature">{feature}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

const venues = [
  {
    name: "Sun-Moon Lake",
    location: "Quebec",
    image: "/images/image-1.jpg",
    description: "Sun Moon Lake National Scenic Area has a rich indigenous culture, and excellent agricultural products. Come here to enjoy bike riding, cable car and boat rides, or take the little train at Jiji and experience the nostalgic Taiwan railway.",
    price: "500",
    discount: "15%",
    features: ["Dogs welcome", "Up to 20+ guests", "Bath", "BBQ"]
  },
  {
    name: "Beanfield Centre",
    location: "Nova Scotia",
    image: "/images/image-2.jpg",
    description: "Beanfield Centre is Canada’s first LEED Silver conference centre, designed for meetings, conventions and galas. Located in the former Automotive Building, this Art Deco masterpiece offers spectacular lakeside views.",
    price: "425",
    discount: "15%",
    features: ["Up to 20+ guests", "Air Conditioning", "Hosting Venue"]
  },
  {
    name: "Taipei Performing Arts Center",
    location: "Quebec",
    image: "/images/image-3.jpg",
    description: "Stage productions, workshops, talks, courses, tours; we have a wide range of programs and activities for all ages.",
    price: "1500",
    discount: "15%",
    features: ["Dogs welcome", "Up to 20 guests", "Air Conditioning", "Hosting Venue", "Theatre"]
  }
];
