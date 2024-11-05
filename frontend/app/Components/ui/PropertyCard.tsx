import React from "react";

interface PropertyCardProps {
  id: string;
  name: string;
  location: string;
  description: string;
  amenities: string[];
  rating: number;
  price: string;
  priceUnit: string;
  imageUrl: string;
  condition?: string;
}

const PropertyCard: React.FC<PropertyCardProps> = ({
  name,
  location,
  description,
  amenities,
  rating,
  price,
  priceUnit,
  imageUrl,
  condition,
}) => {
  return (
    <div className="border rounded-lg shadow-md overflow-hidden">
      <img
        src={imageUrl}
        alt={name}
        className="w-full h-48 object-cover"
        onError={(e) => {
          e.currentTarget.src = "/Public/Image/apartment.svg"; 
        }}
      />
      <div className="p-4">
        <h3 className="text-xl font-semibold">{name}</h3>
        <p className="text-gray-600">{location}</p>
        <p className="mt-2">{description}</p>
        <p className="mt-2">Rating: {rating.toFixed(1)}</p>
        {condition && <p className="mt-1 text-green-600">{condition}</p>}
        <p className="mt-2 font-semibold">
          {price} {priceUnit}
        </p>
        <ul className="mt-2 list-disc pl-5">
          {amenities.map((amenity, index) => (
            <li key={index} className="text-gray-500">
              {amenity}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default PropertyCard;
