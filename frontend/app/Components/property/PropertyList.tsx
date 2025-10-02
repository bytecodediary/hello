import React from 'react';
import PropertyCard from './PropertCard';
import type { PropertyRecord } from '@/app/type/api';

type PropertyListProps = {
  properties: PropertyRecord[];
  onPropertyClick: (slug: string) => void;
};

export default function PropertyList({ properties, onPropertyClick }: PropertyListProps) {
  if (!properties.length) {
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
          key={property.slug}
          property={property}
          onClick={onPropertyClick}
        />
      ))}
    </div>
  );
}