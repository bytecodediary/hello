"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import PropertyCard from "../Components/property/PropertCard";
import type { FavoriteRecord } from "../type/api";
import { ApiError, apiClient } from "../libs/api";
import { useAuth } from "../Pages/API/authCheck";

export default function SavedPropertiesPage() {
  const { user, loading: authLoading } = useAuth();
  const [favorites, setFavorites] = useState<FavoriteRecord[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!user) return;
    apiClient.get<{ results: FavoriteRecord[] }>("/api/v1/favorites/")
      .then((response) => setFavorites(response.results))
      .catch((requestError) => setError(requestError instanceof ApiError ? requestError.message : "Saved properties could not be loaded."));
  }, [user]);

  if (authLoading) return <main className="min-h-screen bg-slate-50 px-6 pb-16 pt-32"><div className="mx-auto max-w-7xl animate-pulse"><div className="h-10 w-64 rounded bg-slate-200" /></div></main>;
  if (!user) return <main className="min-h-screen bg-slate-50 px-6 pb-16 pt-32"><div className="mx-auto max-w-xl rounded-2xl bg-white p-8 text-center shadow-sm"><h1 className="text-2xl font-bold text-slate-950">Your saved properties</h1><p className="mt-2 text-slate-600">Sign in to keep a shortlist while you search.</p><Link href="/login" className="mt-5 inline-block rounded-lg bg-emerald-700 px-5 py-2.5 font-semibold text-white">Sign in</Link></div></main>;

  return <main className="min-h-screen bg-slate-50 px-4 pb-16 pt-28 sm:px-6"><div className="mx-auto max-w-7xl"><h1 className="text-4xl font-bold tracking-tight text-slate-950">Saved properties</h1><p className="mt-2 text-slate-600">Keep the places you want to revisit close.</p>{error && <p role="alert" className="mt-6 rounded-lg bg-red-50 p-4 text-red-800">{error}</p>}{favorites.length ? <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">{favorites.map((favorite) => <PropertyCard key={favorite.id} property={favorite.property_details} onClick={(slug) => window.location.assign(`/properties/${encodeURIComponent(slug)}`)} />)}</div> : <div className="mt-8 rounded-2xl border border-dashed border-slate-300 bg-white p-12 text-center"><h2 className="text-xl font-semibold">Nothing saved yet</h2><p className="mt-2 text-slate-600">Explore the market and save the properties that feel right.</p><Link href="/properties" className="mt-5 inline-block rounded-lg bg-emerald-700 px-5 py-2.5 font-semibold text-white">Explore properties</Link></div>}</div></main>;
}
