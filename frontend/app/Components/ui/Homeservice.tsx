"use client";

import React from 'react';
import Card from './Card';

const Homeservice: React.FC = () => {
    const handleBrowseHomes = () => {
        console.log('Browse Homes clicked');
    };

    const handleSellHome = () => {
        console.log('Sell Home clicked');
    };

    const handleFindRentals = () => {
        console.log('Find Rentals clicked');
    };

    return (
        <div className="bg-slate-200  rounded-lg shadow-md p-6 flex flex-row items-center text-center justify-center">
            <Card
                title="Buy a home"
                description="Find your place with an immersive photo experience and the most listings, including things you won’t find anywhere else."
                buttonText="Browse homes"
                onClick={handleBrowseHomes}
                imageNumber={1}
            />
            <Card
                title="Sell a home"
                description="No matter what path you take to sell your home, we can help you navigate a successful sale."
                buttonText="See your options"
                onClick={handleSellHome}
                imageNumber={2}
            />
             <Card
                title="Rent a home"
                description="We’re creating a seamless online experience—from shopping on the largest rental network, to applying, to paying rent."
                buttonText="Find rentals"
                onClick={handleFindRentals}
                imageNumber={3}
            />
        </div>
    );
};

export default Homeservice;
