export type Property = {
    id: string;
    title: string;
    type: 'house' | 'apartment' | 'condo' | 'townhouse';
    price: number;
    bedrooms: number;
    bathrooms: number;
    sqft: number;
    image: string;
    location: string;
    amenities: string[];
    featured: boolean;
    description?: string;
    yearBuilt?: number;
    parkingSpaces?: number;
    agent?: {
      name: string;
      phone: string;
      email: string;
      image: string;
    };
  };