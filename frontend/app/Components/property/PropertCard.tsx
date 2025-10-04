import React from 'react';
import { Home, Bed, Bath, Square, MapPin } from 'lucide-react';
import { Property } from '@/app/type/property';

type PropertyCardProps = {
  property: Property;
  onClick: (id: string) => void;
};

export default function PropertyCard({ property, onClick }: PropertyCardProps) {
  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 0,
    }).format(price);
  };

  return (
    <div 
      onClick={() => onClick(property.id)}
      className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300 cursor-pointer"
    >
      <div className="relative h-48">
        <img
          src={property.image}
          alt={property.title}
          className="w-full h-full object-cover"
        />
        {property.featured && (
          <span className="absolute top-2 right-2 bg-indigo-600 text-white px-2 py-1 rounded text-xs font-semibold">
            Featured
          </span>
        )}
      </div>
      <div className="p-4">
        <div className="flex justify-between items-start mb-2">
          <h3 className="text-lg font-semibold text-gray-900 mb-1">
            {property.title}
          </h3>
          <span className="text-lg font-bold text-indigo-600">
            {formatPrice(property.price)}
          </span>
        </div>
        <div className="flex items-center text-gray-600 mb-2">
          <MapPin className="h-4 w-4 mr-1" />
          <span className="text-sm">{property.location}</span>
        </div>
        <div className="grid grid-cols-4 gap-2 mb-3">
          <div className="flex items-center text-gray-600">
            <Home className="h-4 w-4 mr-1" />
            <span className="text-sm">{property.type}</span>
          </div>
          <div className="flex items-center text-gray-600">
            <Bed className="h-4 w-4 mr-1" />
            <span className="text-sm">{property.bedrooms}</span>
          </div>
          <div className="flex items-center text-gray-600">
            <Bath className="h-4 w-4 mr-1" />
            <span className="text-sm">{property.bathrooms}</span>
          </div>
          <div className="flex items-center text-gray-600">
            <Square className="h-4 w-4 mr-1" />
            <span className="text-sm">{property.sqft}</span>
          </div>
        </div>
        <div className="flex flex-wrap gap-1">
          {property.amenities.slice(0, 3).map((amenity) => (
            <span
              key={amenity}
              className="bg-gray-100 text-gray-600 px-2 py-1 rounded text-xs"
            >
              {amenity}
            </span>
          ))}
          {property.amenities.length > 3 && (
            <span className="bg-gray-100 text-gray-600 px-2 py-1 rounded text-xs">
              +{property.amenities.length - 3} more
            </span>
          )}
        </div>
      </div>
    </div>
  );
}