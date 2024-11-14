"use client";

import React, { useState, useMemo } from 'react';
import Filters from '@/app/Components/property/filters';
import PropertyList from '@/app/Components/property/PropertyList';
import PropertyDetails from '@/app/Components/property/PropertyDetails';
import { properties } from '@/app/data/properties';
import { Property } from '@/app/type/property';
import Header from '@/app/Components/Layouts/Header';

function Propage() {
  const [filters, setFilters] = useState({
    search: '',
    type: '',
    minPrice: '',
    maxPrice: '',
    sortBy: 'featured',
  });
  const [selectedPropertyId, setSelectedPropertyId] = useState<string | null>(null);

  const handleFilterChange = (name: string, value: string) => {
    setFilters((prev) => ({ ...prev, [name]: value }));
  };

  const filteredProperties = useMemo(() => {
    return properties
      .filter((property) => {
        const matchesSearch = property.title
          .toLowerCase()
          .includes(filters.search.toLowerCase());
        const matchesType = !filters.type || property.type === filters.type;
        const matchesMinPrice =
          !filters.minPrice || property.price >= parseInt(filters.minPrice);
        const matchesMaxPrice =
          !filters.maxPrice || property.price <= parseInt(filters.maxPrice);

        return matchesSearch && matchesType && matchesMinPrice && matchesMaxPrice;
      })
      .sort((a, b) => {
        switch (filters.sortBy) {
          case 'price-asc':
            return a.price - b.price;
          case 'price-desc':
            return b.price - a.price;
          case 'name':
            return a.title.localeCompare(b.title);
          default:
            return b.featured ? 1 : -1;
        }
      });
  }, [filters, properties]);

  const selectedProperty = selectedPropertyId 
    ? properties.find(p => p.id === selectedPropertyId)
    : null;

  return (
    <div className="min-h-screen bg-gray-100">
      <Header/>
      <header className="bg-white shadow-sm py-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-2xl font-bold text-gray-900">Property Listings</h1>
          <p className="mt-1 text-sm text-gray-500">
            Find your perfect property from our curated listings
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {selectedProperty ? (
          <PropertyDetails 
            property={selectedProperty} 
            onBack={() => setSelectedPropertyId(null)}
          />
        ) : (
          <>
            <Filters filters={filters} onFilterChange={handleFilterChange} />
            <PropertyList 
              properties={filteredProperties} 
              onPropertyClick={setSelectedPropertyId}
            />
          </>
        )}
      </main>
    </div>
  );
}

export default Propage;