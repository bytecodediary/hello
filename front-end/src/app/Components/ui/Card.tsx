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


export const Card1: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ className, children, ...props }) => (
    <div className={`border rounded-lg shadow-md ${className}`} {...props}>
      {children}
    </div>
  )

  export const CardHeader: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ className, children, ...props }) => (
    <div className={`p-4 border-b ${className}`} {...props}>
      {children}
    </div>
  )
  
  export const CardContent: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ className, children, ...props }) => (
    <div className={`p-4 ${className}`} {...props}>
      {children}
    </div>
  )

  
  export const CardFooter: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ className, children, ...props }) => (
    <div className={`p-4 border-t ${className}`} {...props}>
      {children}
    </div>
  )
  
  export const CardTitle: React.FC<React.HTMLAttributes<HTMLHeadingElement>> = ({ className, children, ...props }) => (
    <h3 className={`text-lg font-semibold ${className}`} {...props}>
      {children}
    </h3>
  )

  interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: "default" | "destructive";
  }
  

  