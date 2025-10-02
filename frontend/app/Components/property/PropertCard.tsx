import Image from 'next/image';
import { MapPin } from 'lucide-react';
import type { PropertyRecord } from '@/app/type/api';

type PropertyCardProps = {
  property: PropertyRecord;
  onClick: (slug: string) => void;
};

export default function PropertyCard({ property, onClick }: PropertyCardProps) {
  const imageSrc = property.images?.[0]?.image;
  const imageAlt = property.images?.[0]?.image_alt ?? property.title;

  return (
    <button
      type="button"
      onClick={() => onClick(property.slug)}
      className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300 text-left"
    >
      <div className="relative h-48 w-full">
        {imageSrc ? (
          <Image
            src={imageSrc}
            alt={imageAlt}
            fill
            className="object-cover"
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
            unoptimized
          />
        ) : (
          <div className="flex h-full w-full items-center justify-center bg-muted text-muted-foreground">
            No image
          </div>
        )}
        <span className="absolute top-2 right-2 rounded-full bg-primary/90 px-2 py-1 text-xs font-semibold text-white capitalize">
          {property.status}
        </span>
      </div>
      <div className="p-4">
        <div className="flex items-start justify-between gap-2">
          <h3 className="text-lg font-semibold text-gray-900 line-clamp-2">
            {property.title}
          </h3>
          <span className="whitespace-nowrap text-lg font-bold text-primary">
            {Intl.NumberFormat('en-KE', {
              style: 'currency',
              currency: 'KES',
              maximumFractionDigits: 0,
            }).format(property.price)}
          </span>
        </div>
        <div className="mt-2 flex items-center text-gray-600">
          <MapPin className="mr-1 h-4 w-4" />
          <span className="text-sm">
            {[property.address, property.city].filter(Boolean).join(', ')}
          </span>
        </div>
        {property.features && property.features.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-2">
            {property.features.slice(0, 3).map((feature) => (
              <span
                key={feature.feature_name}
                className="rounded-full bg-gray-100 px-2 py-1 text-xs text-gray-700"
              >
                {feature.feature_name}: {feature.feature_value}
              </span>
            ))}
          </div>
        )}
      </div>
    </button>
  );
}