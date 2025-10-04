import { Property } from '../type/property';

export const properties: Property[] = [
  {
    id: '1',
    title: 'Modern Downtown Apartment',
    type: 'apartment',
    price: 450000,
    bedrooms: 2,
    bathrooms: 2,
    sqft: 1200,
    image: 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=800',
    location: 'Downtown',
    amenities: ['Parking', 'Gym', 'Pool', 'Security', 'Elevator', 'Central AC'],
    featured: true,
    description: 'Luxurious downtown apartment featuring modern amenities, stunning city views, and premium finishes throughout.',
    yearBuilt: 2020,
    parkingSpaces: 1,
    agent: {
      name: 'Sarah Johnson',
      phone: '(555) 123-4567',
      email: 'sarah.j@realestate.com',
      image: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?auto=format&fit=crop&w=200'
    }
  },
  {
    id: '2',
    title: 'Luxury Family Home',
    type: 'house',
    price: 850000,
    bedrooms: 4,
    bathrooms: 3,
    sqft: 2800,
    image: 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800',
    location: 'Suburbs',
    amenities: ['Garden', 'Garage', 'Security', 'Smart Home', 'Solar Panels'],
    featured: true,
    description: 'Spectacular family home in a prestigious neighborhood. Features include a gourmet kitchen, spacious master suite, and beautifully landscaped backyard.',
    yearBuilt: 2018,
    parkingSpaces: 2,
    agent: {
      name: 'Michael Chen',
      phone: '(555) 234-5678',
      email: 'michael.c@realestate.com',
      image: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=200'
    }
  },
  {
    id: '3',
    title: 'Cozy Studio Apartment',
    type: 'apartment',
    price: 250000,
    bedrooms: 1,
    bathrooms: 1,
    sqft: 600,
    image: 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=800',
    location: 'Midtown',
    amenities: ['Parking', 'Elevator', 'Storage Unit'],
    featured: false,
    description: 'Efficient and stylish studio apartment perfect for singles or couples. Modern finishes and great location near public transportation.',
    yearBuilt: 2015,
    parkingSpaces: 1,
    agent: {
      name: 'Emily Rodriguez',
      phone: '(555) 345-6789',
      email: 'emily.r@realestate.com',
      image: 'https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?auto=format&fit=crop&w=200'
    }
  },
  {
    id: '4',
    title: 'Waterfront Condo',
    type: 'condo',
    price: 650000,
    bedrooms: 3,
    bathrooms: 2,
    sqft: 1800,
    image: 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800',
    location: 'Waterfront',
    amenities: ['Pool', 'Gym', 'Security', 'Balcony', 'Water View'],
    featured: true,
    description: 'Breathtaking waterfront condo with panoramic views. Featuring high-end appliances, custom cabinetry, and resort-style amenities.',
    yearBuilt: 2019,
    parkingSpaces: 2,
    agent: {
      name: 'David Thompson',
      phone: '(555) 456-7890',
      email: 'david.t@realestate.com',
      image: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=200'
    }
  },
  {
    id: '5',
    title: 'Urban Loft',
    type: 'apartment',
    price: 500000,
    bedrooms: 2,
    bathrooms: 1,
    sqft: 1400,
    image: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800',
    location: 'City Center',
    amenities: ['Gym', 'Security', 'Balcony'],
    featured: false,
    description: 'Spacious urban loft with exposed brick walls and an open floor plan. Ideal for young professionals looking for an edgy yet comfortable space.',
    yearBuilt: 2017,
    parkingSpaces: 1,
    agent: {
      name: 'Alexandra Moore',
      phone: '(555) 567-8901',
      email: 'alexandra.m@realestate.com',
      image: 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=200'
    }
  },
  {
    id: '6',
    title: 'Countryside Villa',
    type: 'house',
    price: 1200000,
    bedrooms: 5,
    bathrooms: 4,
    sqft: 3500,
    image: 'https://images.unsplash.com/photo-1568605114967-8130f3a36994?auto=format&fit=crop&w=800',
    location: 'Countryside',
    amenities: ['Garden', 'Garage', 'Pool', 'Patio', 'Solar Panels'],
    featured: true,
    description: 'Beautiful villa with extensive gardens and a private pool. Perfect for families seeking tranquility in a natural setting.',
    yearBuilt: 2015,
    parkingSpaces: 3,
    agent: {
      name: 'Liam Nguyen',
      phone: '(555) 678-9012',
      email: 'liam.n@realestate.com',
      image: 'https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=200'
    }
  },
  {
    id: '7',
    title: 'Beachfront Bungalow',
    type: 'house',
    price: 700000,
    bedrooms: 3,
    bathrooms: 2,
    sqft: 1500,
    image: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800',
    location: 'Beach',
    amenities: ['Beach Access', 'Balcony', 'Security'],
    featured: true,
    description: 'Charming bungalow with direct beach access. Offers the ultimate getaway experience with unobstructed ocean views.',
    yearBuilt: 2012,
    parkingSpaces: 1,
    agent: {
      name: 'Sophia Williams',
      phone: '(555) 789-0123',
      email: 'sophia.w@realestate.com',
      image: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=200'
    }
  },
  {
    id: '8',
    title: 'Penthouse with Skyline View',
    type: 'apartment',
    price: 950000,
    bedrooms: 3,
    bathrooms: 2,
    sqft: 2200,
    image: 'https://images.unsplash.com/photo-1533002145978-c6e6e4a33a06?auto=format&fit=crop&w=800',
    location: 'Uptown',
    amenities: ['Gym', 'Security', 'Terrace', 'Pool'],
    featured: true,
    description: 'Stunning penthouse apartment with a large terrace overlooking the city skyline. Ideal for luxurious living in a vibrant urban environment.',
    yearBuilt: 2021,
    parkingSpaces: 2,
    agent: {
      name: 'Joshua Brown',
      phone: '(555) 890-1234',
      email: 'joshua.b@realestate.com',
      image: 'https://images.unsplash.com/photo-1525186402429-367a1d5bc53d?auto=format&fit=crop&w=200'
    }
  },
  {
    id: '9',
    title: 'Historic Townhouse',
    type: 'townhouse',
    price: 480000,
    bedrooms: 3,
    bathrooms: 2,
    sqft: 1800,
    image: 'https://images.unsplash.com/photo-1599423300746-b62533397364?auto=format&fit=crop&w=800',
    location: 'Old Town',
    amenities: ['Fireplace', 'Garage', 'Garden', 'Patio'],
    featured: true,
    description: 'Charming townhouse with historic character. Features exposed brick walls, a cozy fireplace, and a private garden.',
    yearBuilt: 1920,
    parkingSpaces: 1,
    agent: {
      name: 'Elizabeth White',
      phone: '(555) 901-2345',
      email: 'elizabeth.w@realestate.com',
      image: 'https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?auto=format&fit=crop&w=200'
    }
  },
  {
    id: '10',
    title: 'Lakeside Cabin',
    type: 'house',
    price: 550000,
    bedrooms: 2,
    bathrooms: 1,
    sqft: 1100,
    image: 'https://images.unsplash.com/photo-1599423300746-b62533397364?auto=format&fit=crop&w=800',
    location: 'Lakefront',
    amenities: ['Dock', 'Fireplace', 'Patio', 'Water View'],
    featured: false,
    description: 'Rustic lakeside cabin with private dock and serene views. Perfect for weekend getaways or a cozy lifestyle close to nature.',
    yearBuilt: 1985,
    parkingSpaces: 1,
    agent: {
      name: 'Daniel Cooper',
      phone: '(555) 012-3456',
      email: 'daniel.c@realestate.com',
      image: 'https://images.unsplash.com/photo-1484249170766-998fa6efe3c8?auto=format&fit=crop&w=200'
    }
  }
  // Add more properties following the same structure to complete the list up to 20 properties
];
