import React from 'react';
import PropertyCard from './PropertCard';
import { Property } from '@/app/type/property';

type PropertyListProps = {
  properties: Property[];
  onPropertyClick: (id: string) => void;
};

export default function PropertyList({ properties, onPropertyClick }: PropertyListProps) {
  if (properties.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">No properties found matching your criteria.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {properties.map((property) => (
        <PropertyCard 
          key={property.id} 
          property={property} 
          onClick={onPropertyClick}
        />
      ))}
    </div>
  );
}