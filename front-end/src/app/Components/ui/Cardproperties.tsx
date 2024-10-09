import { Star } from "lucide-react";
import { Button } from "./Button";
import { Card1, CardContent, CardFooter, CardHeader, CardTitle } from "./Card";
import Image from "next/image";

// Import images
import placeholderImage from "../../Public/Image/spot1.webp";

interface Property {
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

const properties: Property[] = [
  {
    id: "1",
    name: "Property Name",
    location: "Suburb from your location",
    description: "Number of bedrooms and bathrooms",
    amenities: ["Free cancellation", "Amenities included"],
    rating: 4.6,
    price: "Price per",
    priceUnit: "3 nights, 2 adults",
    imageUrl: placeholderImage,
  },
  {
    id: "1",
    name: "Property Name",
    location: "Suburb from your location",
    description: "Number of bedrooms and bathrooms",
    amenities: ["Free cancellation", "Amenities included"],
    rating: 4.6,
    price: "Price per",
    priceUnit: "3 nights, 2 adults",
    imageUrl: placeholderImage,
  },
  {
    id: "2",
    name: "Property Name",
    location: "Suburb from your location",
    description: "Number of bedrooms and bathrooms",
    amenities: ["Free cancellation"],
    rating: 4.2,
    price: "Price per",
    priceUnit: "Duration of stay",
    imageUrl: placeholderImage,
  },
  {
    id: "3",
    name: "RealEstateHub Copenhagen",
    location: "2.0 km from city center",
    description: "Premium apartment",
    amenities: ["1 bedroom", "1 bathroom"],
    rating: 3.9,
    price: "$220 per",
    priceUnit: "3 nights, 2 adults",
    imageUrl: placeholderImage,
    condition: "Good condition",
  },
  {
    id: "4",
    name: "RealEstateHub Bonduel",
    location: "Near city center",
    description: "Comfortable apartment",
    amenities: ["1 bedroom", "1 bathroom"],
    rating: 3.1,
    price: "$60 per night",
    priceUnit: "3 nights, 2 adults",
    imageUrl: placeholderImage,
    condition: "Average condition",
  },
];

export default function CardProperties() {
  return (
    <div className="grid gap-3 md:grid-row-2 lg:grid-row-3 bg-white">
      {properties.map((property) => (
        <Card1 key={property.id} className="overflow-hidden">
          <div className="flex">
            <div>
              <Image
                src={property.imageUrl}
                alt={property.name}
                className="h-48 w-full object-cover"
                width={300}
                height={200}
              />
            </div>
            <div>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span>{property.name}</span>
                  <span className="flex items-center text-sm">
                    <Star className="mr-1 h-4 w-4 fill-current" />
                    {property.rating}
                  </span>
                </CardTitle>
                <p className="text-sm text-muted-foreground">
                  {property.location}
                </p>
              </CardHeader>
              <CardContent>
                <p className="text-sm">{property.description}</p>
                <ul className="mt-2 text-sm text-muted-foreground">
                  {property.amenities.map((amenity, index) => (
                    <li key={index}>{amenity}</li>
                  ))}
                </ul>
                {property.condition && (
                  <p className="mt-2 text-sm font-semibold">
                    {property.condition}
                  </p>
                )}
              </CardContent>
            </div>
          </div>

          <CardFooter className="flex flex-col items-center justify-between">
            <div>
              <p className="font-bold">{property.price}</p>
              <p className="text-sm ">{property.priceUnit}</p>
            </div>
            <Button variant="primary" size="lg">
              Contact Stakeholder
            </Button>
          </CardFooter>
        </Card1>
      ))}
    </div>
  );
}
