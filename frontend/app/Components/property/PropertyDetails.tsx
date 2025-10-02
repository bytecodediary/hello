import Image from 'next/image';
import { ArrowLeft, MapPin, Phone, Mail, Home } from 'lucide-react';
import type { PropertyRecord } from '@/app/type/api';

type PropertyDetailsProps = {
  property: PropertyRecord;
  onBack: () => void;
};

export default function PropertyDetails({ property, onBack }: PropertyDetailsProps) {
  const primaryImage = property.images?.[0]?.image;
  const primaryImageAlt = property.images?.[0]?.image_alt ?? property.title;

  const formattedPrice = Intl.NumberFormat('en-KE', {
    style: 'currency',
    currency: 'KES',
    maximumFractionDigits: 0,
  }).format(property.price);

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden">
      <div className="relative h-96">
        <button
          onClick={onBack}
          className="absolute top-4 left-4 z-10 bg-white p-2 rounded-full shadow-lg hover:bg-gray-100"
        >
          <ArrowLeft className="h-6 w-6 text-gray-600" />
        </button>
        {primaryImage ? (
          <Image
            src={primaryImage}
            alt={primaryImageAlt}
            fill
            className="object-cover"
            sizes="100vw"
            unoptimized
          />
        ) : (
          <div className="flex h-full w-full items-center justify-center bg-muted text-muted-foreground">
            No image available
          </div>
        )}
      </div>

      <div className="p-6 space-y-8">
        <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{property.title}</h1>
            <div className="mt-2 flex items-center text-gray-600">
              <MapPin className="mr-2 h-5 w-5" />
              <span>{[property.address, property.city].filter(Boolean).join(', ')}</span>
            </div>
            <div className="mt-2 inline-flex items-center rounded-full bg-primary/10 px-3 py-1 text-sm font-semibold capitalize text-primary">
              {property.status}
            </div>
          </div>
          <div className="text-left md:text-right">
            <div className="text-3xl font-bold text-primary">{formattedPrice}</div>
            <div className="text-sm text-muted-foreground">
              Listed on {new Date(property.listed_at).toLocaleDateString()}
            </div>
          </div>
        </div>

        <section>
          <h2 className="text-xl font-semibold mb-3">Description</h2>
          <p className="text-gray-600 leading-relaxed">
            {property.description || 'No description available for this property.'}
          </p>
        </section>

        {property.features && property.features.length > 0 && (
          <section>
            <h2 className="text-xl font-semibold mb-3">Key Features</h2>
            <div className="flex flex-wrap gap-2">
              {property.features.map((feature) => (
                <span
                  key={feature.feature_name}
                  className="rounded-full bg-gray-100 px-3 py-1 text-sm text-gray-700"
                >
                  {feature.feature_name}: {feature.feature_value}
                </span>
              ))}
            </div>
          </section>
        )}

        {property.owners && property.owners.length > 0 && (
          <section className="border-t pt-6">
            <h2 className="text-xl font-semibold mb-4">Owners</h2>
            <div className="space-y-4">
              {property.owners.map((owner) => (
                <div key={owner.id} className="flex items-start justify-between gap-4 rounded-lg border p-4">
                  <div>
                    <div className="flex items-center gap-2 text-gray-900">
                      <Home className="h-4 w-4" />
                      <span>{owner.user}</span>
                    </div>
                    {owner.property_details && (
                      <p className="mt-1 text-sm text-muted-foreground">
                        {owner.property_details}
                      </p>
                    )}
                  </div>
                  <div className="space-y-2 text-sm text-gray-600">
                    {owner.phone_number && (
                      <div className="flex items-center gap-2">
                        <Phone className="h-4 w-4" />
                        <span>{owner.phone_number}</span>
                      </div>
                    )}
                    {property.city && (
                      <div className="flex items-center gap-2">
                        <MapPin className="h-4 w-4" />
                        <span>{property.city}</span>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        <section className="border-t pt-6">
          <h2 className="text-xl font-semibold mb-4">Contact</h2>
          <div className="space-y-3 text-sm text-gray-700">
            <div className="flex items-center gap-2">
              <Phone className="h-4 w-4" />
              <span>Reach out to our team to schedule a viewing.</span>
            </div>
            <div className="flex items-center gap-2">
              <Mail className="h-4 w-4" />
              <span>info@realestatehub.com</span>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}