"use client"; 

import React from 'react';
import Image from 'next/image';
import Spot1 from '../../Public/Image/spot1.webp';
import Spot2 from '../../Public/Image/spot2.webp';
import Spot3 from '../../Public/Image/spot3.webp';

interface CardProps {
    title: string;
    description: string;
    buttonText: string;
    onClick: () => void;
    imageNumber: number;
}

const Card: React.FC<CardProps> = ({ title, description, buttonText, onClick, imageNumber }) => {
    const getImageSrc = () => {
        switch (imageNumber) {
            case 1:
                return Spot1;
            case 2:
                return Spot2;
            case 3:
                return Spot3;
            default:
                return Spot1;
        }
    };

    return (
        <div className="card  md:grid-cols-2 lg:grid-cols-3 gap-8 ml-5 min-h-96">
            <div className="icon px-10">
                <Image src={getImageSrc()} alt={title} width={140} height={140} />
            </div>
            <h2 className='text-black font-bold'>{title}</h2>
            <p className='text-black'>{description}</p>
            <button onClick={onClick} className='text-red '>{buttonText}</button>
        </div>
    );
};

export default Card;
