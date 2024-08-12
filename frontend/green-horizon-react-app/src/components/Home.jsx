import React from 'react';
import './Home.css';
import Banner from './Banner'
import Card from './Card'
import venue1 from "../assets/venue1.jpg"
import venue2 from "../assets/venue2.png"
import venue3 from "../assets/venue3.jpg"

// ES7 snippets to do 'rfce'

function Home() {
    return (
        <div className='home'>
            <Banner />

            <div className='home__section'>
            <Card
                src="https://a0.muscache.com/im/pictures/eb9c7c6a-ee33-414a-b1ba-14e8860d59b3.jpg?im_w=720"
                title="Online Experiences"
                description="Unique activities we can do together, led by a world of hosts."
            />
            <Card
                src="https://a0.muscache.com/im/pictures/15159c9c-9cf1-400e-b809-4e13f286fa38.jpg?im_w=720"
                title="Unique venues"
                description="Spaces that are more than just a place to hose your event."
            />
            <Card
                src="https://a0.muscache.com/im/pictures/fdb46962-10c1-45fc-a228-d0b055411448.jpg?im_w=720"
                title="Green venues"
                description="Comfortable private places to host your events, ENVIRONMENTALLY."
            />
            </div>
            <div className='home__section'>
            <Card
                src={venue1}
                title="Calgary Corporate Event Venue"
                description="Plan your next corporate event in an event space that is all yours"
                price="Starting from £130"
            />
            <Card
                src={venue2}
                title="LaunchPad Golf"
                description="The newly renovated West Canada venues for corporate parties"
                price="Starting from £350"
            />
            <Card
                src={venue3}
                title="Westin Ottawa"
                description="Professional planning services, flexible meeting venues and more..."
                price="Starting from £470"
            />
            </div>
        </div>
    )
}

export default Home
