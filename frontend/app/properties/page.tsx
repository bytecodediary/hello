"use client";

import Link from "next/link";
import { Suspense, useEffect, useMemo, useState } from "react";
import { usePathname, useRouter, useSearchParams } from "next/navigation";

import PropertyCard from "../Components/property/PropertCard";
import type { PaginatedResponse, PropertyRecord } from "../type/api";
import { ApiError, apiClient } from "../libs/api";

type SearchState = {
  search: string;
  listing_type: string;
  property_type: string;
  city: string;
  min_price: string;
  max_price: string;
  min_bedrooms: string;
  ordering: string;
};

const emptySearch: SearchState = {
  search: "",
  listing_type: "",
  property_type: "",
  city: "",
  min_price: "",
  max_price: "",
  min_bedrooms: "",
  ordering: "-listed_at",
};

function PropertiesContent() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const queryString = searchParams.toString();
  const [filters, setFilters] = useState<SearchState>(emptySearch);
  const [data, setData] = useState<PaginatedResponse<PropertyRecord> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const currentPage = useMemo(() => searchParams.get("page") ?? "1", [searchParams]);

  useEffect(() => {
    setFilters({
      search: searchParams.get("search") ?? "",
      listing_type: searchParams.get("listing_type") ?? "",
      property_type: searchParams.get("property_type") ?? "",
      city: searchParams.get("city") ?? "",
      min_price: searchParams.get("min_price") ?? "",
      max_price: searchParams.get("max_price") ?? "",
      min_bedrooms: searchParams.get("min_bedrooms") ?? "",
      ordering: searchParams.get("ordering") ?? "-listed_at",
    });

    const controller = new AbortController();
    setLoading(true);
    setError(null);
    apiClient
      .get<PaginatedResponse<PropertyRecord>>("/api/v1/listings/", {
        authenticated: false,
        query: {
          search: searchParams.get("search"),
          listing_type: searchParams.get("listing_type"),
          property_type: searchParams.get("property_type"),
          city: searchParams.get("city"),
          min_price: searchParams.get("min_price"),
          max_price: searchParams.get("max_price"),
          min_bedrooms: searchParams.get("min_bedrooms"),
          ordering: searchParams.get("ordering") ?? "-listed_at",
          page: searchParams.get("page") ?? "1",
        },
        signal: controller.signal,
      })
      .then(setData)
      .catch((requestError: unknown) => {
        if (requestError instanceof DOMException && requestError.name === "AbortError") return;
        setError(requestError instanceof ApiError ? requestError.message : "Properties could not be loaded.");
      })
      .finally(() => setLoading(false));

    return () => controller.abort();
  }, [queryString, searchParams]);

  function applyFilters(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const next = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value && !(key === "ordering" && value === "-listed_at")) next.set(key, value);
    });
    router.push(`${pathname}${next.toString() ? `?${next.toString()}` : ""}`);
  }

  function resetFilters() {
    setFilters(emptySearch);
    router.push(pathname);
  }

  function movePage(url: string | null) {
    if (!url) return;
    const nextUrl = new URL(url);
    router.push(`${pathname}${nextUrl.search}`);
  }

  return (
    <main className="min-h-screen bg-slate-50 px-4 pb-16 pt-28 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">
        <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="mb-2 text-sm font-semibold uppercase tracking-[0.2em] text-emerald-700">Kenya property market</p>
            <h1 className="text-4xl font-bold tracking-tight text-slate-950">Find a place that fits your life.</h1>
            <p className="mt-3 max-w-2xl text-slate-600">Explore trusted homes, land, and commercial spaces for sale or long-term rent.</p>
          </div>
          <Link href="/saved" className="text-sm font-semibold text-emerald-700 hover:text-emerald-800">View saved properties →</Link>
        </div>

        <form onSubmit={applyFilters} className="mb-8 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:p-6">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <label className="lg:col-span-2">
              <span className="mb-1 block text-sm font-medium text-slate-700">Search</span>
              <input value={filters.search} onChange={(event) => setFilters({ ...filters, search: event.target.value })} placeholder="Kilimani, apartment, garden…" className="w-full rounded-lg border border-slate-300 px-3 py-2.5 outline-none ring-emerald-500 focus:ring-2" />
            </label>
            <label>
              <span className="mb-1 block text-sm font-medium text-slate-700">Purpose</span>
              <select value={filters.listing_type} onChange={(event) => setFilters({ ...filters, listing_type: event.target.value })} className="w-full rounded-lg border border-slate-300 px-3 py-2.5 outline-none ring-emerald-500 focus:ring-2">
                <option value="">Sale or rent</option>
                <option value="sale">For sale</option>
                <option value="rent">For rent</option>
              </select>
            </label>
            <label>
              <span className="mb-1 block text-sm font-medium text-slate-700">Property type</span>
              <select value={filters.property_type} onChange={(event) => setFilters({ ...filters, property_type: event.target.value })} className="w-full rounded-lg border border-slate-300 px-3 py-2.5 outline-none ring-emerald-500 focus:ring-2">
                <option value="">Any type</option>
                <option value="house">House</option>
                <option value="apartment">Apartment</option>
                <option value="townhouse">Townhouse</option>
                <option value="land">Land</option>
                <option value="commercial">Commercial</option>
              </select>
            </label>
            <label>
              <span className="mb-1 block text-sm font-medium text-slate-700">City or town</span>
              <input value={filters.city} onChange={(event) => setFilters({ ...filters, city: event.target.value })} placeholder="Nairobi" className="w-full rounded-lg border border-slate-300 px-3 py-2.5 outline-none ring-emerald-500 focus:ring-2" />
            </label>
            <label>
              <span className="mb-1 block text-sm font-medium text-slate-700">Minimum price</span>
              <input type="number" min="0" value={filters.min_price} onChange={(event) => setFilters({ ...filters, min_price: event.target.value })} placeholder="0" className="w-full rounded-lg border border-slate-300 px-3 py-2.5 outline-none ring-emerald-500 focus:ring-2" />
            </label>
            <label>
              <span className="mb-1 block text-sm font-medium text-slate-700">Maximum price</span>
              <input type="number" min="0" value={filters.max_price} onChange={(event) => setFilters({ ...filters, max_price: event.target.value })} placeholder="Any" className="w-full rounded-lg border border-slate-300 px-3 py-2.5 outline-none ring-emerald-500 focus:ring-2" />
            </label>
            <label>
              <span className="mb-1 block text-sm font-medium text-slate-700">Bedrooms</span>
              <select value={filters.min_bedrooms} onChange={(event) => setFilters({ ...filters, min_bedrooms: event.target.value })} className="w-full rounded-lg border border-slate-300 px-3 py-2.5 outline-none ring-emerald-500 focus:ring-2">
                <option value="">Any</option>
                <option value="1">1+</option>
                <option value="2">2+</option>
                <option value="3">3+</option>
                <option value="4">4+</option>
              </select>
            </label>
            <label>
              <span className="mb-1 block text-sm font-medium text-slate-700">Sort</span>
              <select value={filters.ordering} onChange={(event) => setFilters({ ...filters, ordering: event.target.value })} className="w-full rounded-lg border border-slate-300 px-3 py-2.5 outline-none ring-emerald-500 focus:ring-2">
                <option value="-listed_at">Newest</option>
                <option value="listed_at">Oldest</option>
                <option value="price">Price: low to high</option>
                <option value="-price">Price: high to low</option>
              </select>
            </label>
          </div>
          <div className="mt-5 flex flex-wrap gap-3">
            <button type="submit" className="rounded-lg bg-emerald-700 px-5 py-2.5 text-sm font-semibold text-white hover:bg-emerald-800">Search properties</button>
            <button type="button" onClick={resetFilters} className="rounded-lg border border-slate-300 px-5 py-2.5 text-sm font-semibold text-slate-700 hover:bg-slate-50">Reset</button>
          </div>
        </form>

        {loading ? <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3"><div className="h-80 animate-pulse rounded-2xl bg-slate-200" /><div className="h-80 animate-pulse rounded-2xl bg-slate-200" /><div className="h-80 animate-pulse rounded-2xl bg-slate-200" /></div> : error ? (
          <div role="alert" className="rounded-2xl border border-red-200 bg-red-50 p-6 text-red-800">{error}. Try adjusting your search.</div>
        ) : data?.results.length ? (
          <>
            <div className="mb-4 flex items-center justify-between text-sm text-slate-600"><span>{data.count} properties found</span><span>Page {currentPage}</span></div>
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {data.results.map((property) => <PropertyCard key={property.slug} property={property} onClick={(slug) => router.push(`/properties/${encodeURIComponent(slug)}`)} />)}
            </div>
            <div className="mt-8 flex justify-center gap-3">
              <button disabled={!data.previous} onClick={() => movePage(data.previous)} className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-semibold disabled:cursor-not-allowed disabled:opacity-40">Previous</button>
              <button disabled={!data.next} onClick={() => movePage(data.next)} className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-semibold disabled:cursor-not-allowed disabled:opacity-40">Next</button>
            </div>
          </>
        ) : <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-12 text-center"><h2 className="text-xl font-semibold text-slate-900">No matching properties</h2><p className="mt-2 text-slate-600">Try a wider location or price range.</p><button onClick={resetFilters} className="mt-5 rounded-lg bg-emerald-700 px-5 py-2.5 text-sm font-semibold text-white">Clear filters</button></div>}
      </div>
    </main>
  );
}

export default function PropertiesPage() {
  return <Suspense fallback={<main className="min-h-screen bg-slate-50 px-6 pb-16 pt-32"><div className="mx-auto max-w-7xl animate-pulse"><div className="h-12 w-1/2 rounded bg-slate-200" /></div></main>}><PropertiesContent /></Suspense>;
}
