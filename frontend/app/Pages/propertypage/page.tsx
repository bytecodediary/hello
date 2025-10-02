"use client";

import React, { useCallback, useEffect, useMemo, useState } from 'react';
import Filters from '@/app/Components/property/filters';
import PropertyList from '@/app/Components/property/PropertyList';
import PropertyDetails from '@/app/Components/property/PropertyDetails';
import Header from '@/app/Components/Layouts/Header';
import { apiClient } from '@/app/libs/api';
import type { PropertyRecord } from '@/app/type/api';

function Propage() {
  const [filters, setFilters] = useState({
    search: '',
    city: '',
    status: '',
    minPrice: '',
    maxPrice: '',
    sortBy: 'listed-newest',
  });
  const [properties, setProperties] = useState<PropertyRecord[]>([]);
  const [selectedPropertySlug, setSelectedPropertySlug] = useState<string | null>(null);
  const [selectedProperty, setSelectedProperty] = useState<PropertyRecord | null>(null);
  const [loading, setLoading] = useState(false);
  const [detailLoading, setDetailLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [detailError, setDetailError] = useState<string | null>(null);

  const handleFilterChange = (name: string, value: string) => {
    setFilters((prev) => ({ ...prev, [name]: value }));
  };

  const sortOptionToOrdering = (value: string) => {
    switch (value) {
      case 'price-asc':
        return 'price';
      case 'price-desc':
        return '-price';
      case 'listed-oldest':
        return 'listed_at';
      case 'listed-newest':
      default:
        return '-listed_at';
    }
  };

  const fetchProperties = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const query: Record<string, string> = {};
      if (filters.search) query.search = filters.search;
      if (filters.city) query.city = filters.city;
      if (filters.status) query.status = filters.status;
      if (filters.minPrice) query.min_price = filters.minPrice;
      if (filters.maxPrice) query.max_price = filters.maxPrice;
      query.ordering = sortOptionToOrdering(filters.sortBy);

      const response = await apiClient.get<PropertyRecord[] | { results: PropertyRecord[] }>(
        '/propertylist/',
        {
          authenticated: false,
          query,
        }
      );

      const records = Array.isArray(response) ? response : response?.results ?? [];
      setProperties(records);
    } catch (err) {
      console.error('Failed to fetch properties', err);
      setError(err instanceof Error ? err.message : 'Failed to load properties');
    } finally {
      setLoading(false);
    }
  }, [filters]);

  const fetchPropertyDetail = useCallback(async (slug: string) => {
    try {
      setDetailLoading(true);
      setDetailError(null);
      const record = await apiClient.get<PropertyRecord>(`/property/${slug}/`, {
        authenticated: false,
      });
      setSelectedProperty(record);
    } catch (err) {
      console.error('Failed to fetch property detail', err);
      setDetailError(err instanceof Error ? err.message : 'Failed to load property details');
    } finally {
      setDetailLoading(false);
    }
  }, []);

  useEffect(() => {
    void fetchProperties();
  }, [fetchProperties]);

  useEffect(() => {
    if (!selectedPropertySlug) {
      setSelectedProperty(null);
      return;
    }
    void fetchPropertyDetail(selectedPropertySlug);
  }, [fetchPropertyDetail, selectedPropertySlug]);

  const handlePropertyClick = useCallback((slug: string) => {
    setSelectedPropertySlug(slug);
  }, []);

  const listHeading = useMemo(() => {
    const segments: string[] = [];
    if (filters.city) segments.push(filters.city);
    if (filters.status) segments.push(filters.status);
    if (filters.search) segments.push(`matching "${filters.search}"`);
    return segments.length ? segments.join(' • ') : 'All properties';
  }, [filters.city, filters.status, filters.search]);

  return (
    <div className="min-h-screen bg-gray-100">
      <Header/>
      <header className="bg-white shadow-sm py-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-2xl font-bold text-gray-900">Property Listings</h1>
          <p className="mt-1 text-sm text-gray-500">{listHeading}</p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {selectedProperty ? (
          <div className="space-y-4">
            {detailError && (
              <div className="rounded-md border border-destructive bg-destructive/10 p-4 text-destructive">
                {detailError}
              </div>
            )}
            <PropertyDetails 
              property={selectedProperty} 
              onBack={() => setSelectedPropertySlug(null)}
            />
            {detailLoading && (
              <div className="rounded-md border bg-muted/40 p-4 text-sm text-muted-foreground">
                Loading property details...
              </div>
            )}
          </div>
        ) : (
          <>
            <Filters filters={filters} onFilterChange={handleFilterChange} />
            {error && (
              <div className="mb-4 rounded-md border border-destructive bg-destructive/10 p-4 text-destructive">
                {error}
              </div>
            )}
            <PropertyList 
              properties={properties} 
              onPropertyClick={handlePropertyClick}
            />
            {loading && (
              <div className="mt-4 rounded-md border bg-muted/40 p-4 text-sm text-muted-foreground">
                Loading properties...
              </div>
            )}
          </>
        )}
      </main>
    </div>
  );
}

export default Propage;