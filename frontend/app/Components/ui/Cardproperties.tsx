import Image from "next/image";
import { Card1, CardContent, CardFooter, CardHeader, CardTitle } from "./Card";
import { Button } from "./Button";
import placeholderImage from "../../Public/Image/spot1.webp";
import type { PropertyRecord } from "@/app/type/api";

interface CardPropertiesProps {
  properties?: PropertyRecord[];
  loading?: boolean;
  error?: string | null;
}

export default function CardProperties({
  properties = [],
  loading = false,
  error = null,
}: CardPropertiesProps) {
  if (loading) {
    return (
      <div className="grid gap-3 bg-white">
        <div className="animate-pulse rounded-md bg-muted h-48" />
        <div className="animate-pulse rounded-md bg-muted h-48" />
        <div className="animate-pulse rounded-md bg-muted h-48" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-md border border-destructive/50 bg-destructive/10 p-4 text-destructive">
        {error}
      </div>
    );
  }

  if (!properties.length) {
    return (
      <div className="rounded-md border border-dashed p-6 text-center text-muted-foreground">
        No properties found for the selected filters.
      </div>
    );
  }

  return (
    <div className="grid gap-3 bg-white">
      {properties.map((property) => {
        const imageSrc = property.images?.[0]?.image ?? placeholderImage;
        const imageAlt = property.images?.[0]?.image_alt ?? property.title;
        const propertyStatus = property.status ?? "available";

        return (
          <Card1 key={property.slug} className="overflow-hidden">
            <div className="flex flex-col md:flex-row">
              <div className="md:w-1/3">
                <Image
                  src={imageSrc}
                  alt={imageAlt}
                  className="h-48 w-full object-cover"
                  width={300}
                  height={200}
                  unoptimized={typeof imageSrc === "string"}
                />
              </div>
              <div className="md:w-2/3">
                <CardHeader>
                  <CardTitle className="flex flex-col justify-between gap-2 md:flex-row md:items-center">
                    <span>{property.title}</span>
                    <span className="flex items-center text-xs uppercase tracking-wide text-muted-foreground">
                      <span className="mr-1 inline-block h-2 w-2 rounded-full bg-primary/70" />
                      {propertyStatus}
                    </span>
                  </CardTitle>
                  <p className="text-sm text-muted-foreground">
                    {property.address}, {property.city}
                  </p>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    {property.description}
                  </p>
                  {property.features && property.features.length > 0 && (
                    <ul className="mt-2 text-sm text-muted-foreground">
                      {property.features.slice(0, 4).map((feature) => (
                        <li key={feature.feature_name}>
                          {feature.feature_name}: {feature.feature_value}
                        </li>
                      ))}
                    </ul>
                  )}
                </CardContent>
              </div>
            </div>

            <CardFooter className="flex flex-col items-start justify-between gap-4 border-t p-4 md:flex-row md:items-center">
              <div>
                <p className="text-2xl font-bold text-primary">
                  {Intl.NumberFormat("en-KE", {
                    style: "currency",
                    currency: "KES",
                    maximumFractionDigits: 0,
                  }).format(property.price)}
                </p>
                <p className="text-sm text-muted-foreground">
                  Listed on {new Date(property.listed_at).toLocaleDateString()}
                </p>
              </div>
              <Button variant="primary" size="lg">
                Contact Stakeholder
              </Button>
            </CardFooter>
          </Card1>
        );
      })}
    </div>
  );
}
