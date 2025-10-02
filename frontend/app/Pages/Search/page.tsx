"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import Header from "@/app/Components/Layouts/Header";
import CardProperties from "@/app/Components/ui/Cardproperties";
import PropertySearch from "./Property-search";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/app/Components/ui/select";
import { apiClient } from "@/app/libs/api";
import type { PropertyRecord } from "@/app/type/api";

type SortOption = "listed_at" | "-listed_at" | "price" | "-price";

export default function Buy() {
  const [fix, setFix] = useState(false);
  const [location, setLocation] = useState("");
  const [properties, setProperties] = useState<PropertyRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sortOption, setSortOption] = useState<SortOption>("-listed_at");

  const setFixedSidebar = () => {
    const scrollY = window.scrollY;
    if (scrollY >= 150 && !fix) {
      setFix(true);
    } else if (scrollY < 150 && fix) {
      setFix(false);
    }
  };

  useEffect(() => {
    window.addEventListener("scroll", setFixedSidebar);
    return () => {
      window.removeEventListener("scroll", setFixedSidebar);
    };
  }, []);

  const fetchProperties = useCallback(
    async (opts?: { city?: string }) => {
      try {
        setLoading(true);
        setError(null);

        const query: Record<string, string> = {};
        if (opts?.city) {
          query.city = opts.city;
        }
        if (sortOption) {
          query.ordering = sortOption;
        }

        const response = await apiClient.get<PropertyRecord[] | { results: PropertyRecord[] }>(
          "/propertylist/",
          {
            authenticated: false,
            query,
          }
        );

        const records = Array.isArray(response)
          ? response
          : response?.results ?? [];

        setProperties(records);
      } catch (err) {
        console.error("Failed to load properties", err);
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load properties. Please try again."
        );
      } finally {
        setLoading(false);
      }
    },
    [sortOption]
  );

  useEffect(() => {
    void fetchProperties();
  }, [fetchProperties]);

  const handleSearchSubmit = useCallback(() => {
    void fetchProperties({ city: location || undefined });
  }, [fetchProperties, location]);

  const handleSortChange = useCallback(
    (value: string) => {
      const sortValue = ((): SortOption => {
        switch (value) {
          case "price-asc":
            return "price";
          case "price-desc":
            return "-price";
          case "listed-newest":
            return "-listed_at";
          case "listed-oldest":
            return "listed_at";
          default:
            return "-listed_at";
        }
      })();

      setSortOption(sortValue);
    },
    []
  );

  useEffect(() => {
    void fetchProperties({ city: location || undefined });
  }, [fetchProperties, sortOption]);

  const resultsTitle = useMemo(() => {
    if (!properties.length) {
      return "No results";
    }

    return `${properties.length} result${properties.length === 1 ? "" : "s"}`;
  }, [properties]);

  const locationLabel = location ? `Properties in ${location}` : "Available properties";

  return (
    <div>
      <Header />
      <section className="mt-9">
        <div className="flex flex-grow border-2 max-h-full  ">
          <div
            className={`w-1/3 p-4 border-2 shadow-lg ${
              fix ? " fixed  h-screen" : "sidebar"
            }`}
          >
            <PropertySearch
              location={location}
              onLocationChange={setLocation}
              onSubmit={handleSearchSubmit}
              loading={loading}
            />
          </div>
          <div
            className={`w-2/3 p-4 border-2 shadow-lg ${
              fix ? "ml-[33.33%]" : ""
            }`}
          >
            <div className="bg-[#f8faf8] p-4 rounded-lg">
              <div className="flex justify-between items-center">
                <div>
                  <p className="text-sm text-gray-600 mb-1">
                    {resultsTitle}
                  </p>
                  <h1 className="text-2xl font-bold">{locationLabel}</h1>
                </div>
                <div>
                  <Select
                    defaultValue="listed-newest"
                    onValueChange={handleSortChange}
                  >
                    <SelectTrigger className="w-[180px]">
                      <SelectValue placeholder="Sort by" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="listed-newest">Newest</SelectItem>
                      <SelectItem value="listed-oldest">Oldest</SelectItem>
                      <SelectItem value="price-asc">Price: Low to High</SelectItem>
                      <SelectItem value="price-desc">Price: High to Low</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </div>
            <CardProperties
              properties={properties}
              loading={loading}
              error={error}
            />
          </div>
          {/* <PaginationBar currentPage={2} totalPages={99} /> */}
        </div>
      </section>
      {/* <Footer /> */}
    </div>
  );
}
