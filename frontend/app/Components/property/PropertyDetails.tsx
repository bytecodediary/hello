import React from 'react';
import { Property } from '@/app/type/property';
import { 
  Home, 
  Bed, 
  Bath, 
  Square, 
  MapPin, 
  Calendar, 
  Car,
  Phone,
  Mail,
  ArrowLeft
} from 'lucide-react';

type PropertyDetailsProps = {
  property: Property;
  onBack: () => void;
};

export default function PropertyDetails({ property, onBack }: PropertyDetailsProps) {
  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 0,
    }).format(price);
  };

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden">
      <div className="relative h-96">
        <button
          onClick={onBack}
          className="absolute top-4 left-4 z-10 bg-white p-2 rounded-full shadow-lg hover:bg-gray-100"
        >
          <ArrowLeft className="h-6 w-6 text-gray-600" />
        </button>
        <img
          src={property.image}
          alt={property.title}
          className="w-full h-full object-cover"
        />
      </div>
      
      <div className="p-6">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{property.title}</h1>
            <div className="flex items-center mt-2">
              <MapPin className="h-5 w-5 text-gray-500 mr-2" />
              <span className="text-gray-600">{property.location}</span>
            </div>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold text-indigo-600">
              {formatPrice(property.price)}
            </div>
            {property.featured && (
              <span className="bg-indigo-600 text-white px-3 py-1 rounded-full text-sm mt-2 inline-block">
                Featured
              </span>
            )}
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="flex items-center p-3 bg-gray-50 rounded-lg">
            <Bed className="h-6 w-6 text-gray-500 mr-2" />
            <div>
              <div className="text-sm text-gray-500">Bedrooms</div>
              <div className="font-semibold">{property.bedrooms}</div>
            </div>
          </div>
          <div className="flex items-center p-3 bg-gray-50 rounded-lg">
            <Bath className="h-6 w-6 text-gray-500 mr-2" />
            <div>
              <div className="text-sm text-gray-500">Bathrooms</div>
              <div className="font-semibold">{property.bathrooms}</div>
            </div>
          </div>
          <div className="flex items-center p-3 bg-gray-50 rounded-lg">
            <Square className="h-6 w-6 text-gray-500 mr-2" />
            <div>
              <div className="text-sm text-gray-500">Square Feet</div>
              <div className="font-semibold">{property.sqft}</div>
            </div>
          </div>
          <div className="flex items-center p-3 bg-gray-50 rounded-lg">
            <Car className="h-6 w-6 text-gray-500 mr-2" />
            <div>
              <div className="text-sm text-gray-500">Parking</div>
              <div className="font-semibold">{property.parkingSpaces} spaces</div>
            </div>
          </div>
        </div>

        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-3">Description</h2>
          <p className="text-gray-600 leading-relaxed">{property.description}</p>
        </div>

        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-3">Features & Amenities</h2>
          <div className="flex flex-wrap gap-2">
            {property.amenities.map((amenity) => (
              <span
                key={amenity}
                className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm"
              >
                {amenity}
              </span>
            ))}
          </div>
        </div>

        <div className="border-t pt-6">
          <h2 className="text-xl font-semibold mb-4">Contact Agent</h2>
          {property.agent && (
            <div className="flex items-start space-x-4">
              <img
                src={property.agent.image}
                alt={property.agent.name}
                className="w-16 h-16 rounded-full object-cover"
              />
              <div>
                <h3 className="font-semibold text-lg">{property.agent.name}</h3>
                <div className="space-y-2 mt-2">
                  <div className="flex items-center text-gray-600">
                    <Phone className="h-4 w-4 mr-2" />
                    <span>{property.agent.phone}</span>
                  </div>
                  <div className="flex items-center text-gray-600">
                    <Mail className="h-4 w-4 mr-2" />
                    <span>{property.agent.email}</span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}