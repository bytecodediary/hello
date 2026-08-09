"use client";

import Link from "next/link";
import { useCallback, useEffect, useState, type FormEvent } from "react";

import { ApiError, apiClient } from "../../libs/api";
import { useAuth } from "../../Pages/API/authCheck";
import type { InquiryRecord, PaginatedResponse, PropertyRecord } from "../../type/api";

type ProviderApplication = {
  id: number;
  requested_type: "agent" | "landlord";
  organization_name: string;
  phone_number: string | null;
  message: string;
  status: "pending" | "approved" | "rejected";
  review_notes: string;
};

const blankListing = {
  title: "",
  description: "",
  city: "Nairobi",
  county: "Nairobi",
  neighborhood: "",
  address: "",
  price: "",
  listing_type: "rent",
  property_type: "apartment",
  bedrooms: "1",
  bathrooms: "1",
};

const inquiryStatuses = ["new", "contacted", "scheduled", "completed", "declined", "closed"];

export default function ProviderListingsPage() {
  const { user, loading: authLoading } = useAuth();
  const [applications, setApplications] = useState<ProviderApplication[]>([]);
  const [listings, setListings] = useState<PropertyRecord[]>([]);
  const [inquiries, setInquiries] = useState<InquiryRecord[]>([]);
  const [listing, setListing] = useState(blankListing);
  const [application, setApplication] = useState({ requested_type: "landlord", organization_name: "", phone_number: "", message: "" });
  const [responses, setResponses] = useState<Record<number, string>>({});
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const load = useCallback(async () => {
    if (!user) return;

    try {
      const applicationResponse = await apiClient.get<{ results: ProviderApplication[] }>("/user/api/v1/provider/applications/");
      setApplications(applicationResponse.results);

      if (user.provider_status === "approved") {
        const [listingResponse, inquiryResponse] = await Promise.all([
          apiClient.get<PaginatedResponse<PropertyRecord>>("/api/v1/provider/listings/"),
          apiClient.get<PaginatedResponse<InquiryRecord>>("/api/v1/provider/inquiries/"),
        ]);
        setListings(listingResponse.results);
        setInquiries(inquiryResponse.results);
      }
    } catch (requestError) {
      setError(requestError instanceof ApiError ? requestError.message : "Provider data could not be loaded.");
    }
  }, [user]);

  useEffect(() => {
    void load();
  }, [load]);

  async function submitApplication(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      await apiClient.post("/user/api/v1/provider/applications/", { body: application });
      setMessage("Your provider application has been submitted for review.");
      await load();
    } catch (requestError) {
      setError(requestError instanceof ApiError ? requestError.message : "The application could not be submitted.");
    } finally {
      setSubmitting(false);
    }
  }

  async function submitListing(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      await apiClient.post("/api/v1/provider/listings/", {
        body: {
          ...listing,
          price: Number(listing.price),
          bedrooms: Number(listing.bedrooms),
          bathrooms: Number(listing.bathrooms),
        },
      });
      setMessage("Listing submitted. It will appear publicly after admin review.");
      setListing(blankListing);
      await load();
    } catch (requestError) {
      setError(requestError instanceof ApiError ? requestError.message : "The listing could not be submitted.");
    } finally {
      setSubmitting(false);
    }
  }

  async function updateInquiry(inquiry: InquiryRecord, status: string) {
    setError(null);
    try {
      const updated = await apiClient.patch<InquiryRecord>(`/api/v1/provider/inquiries/${inquiry.id}/`, {
        body: { status, provider_response: responses[inquiry.id] ?? inquiry.provider_response },
      });
      setInquiries((current) => current.map((item) => (item.id === updated.id ? updated : item)));
      setResponses((current) => ({ ...current, [inquiry.id]: updated.provider_response }));
      setMessage("Inquiry updated and the seeker has been notified.");
    } catch (requestError) {
      setError(requestError instanceof ApiError ? requestError.message : "The inquiry could not be updated.");
    }
  }

  if (authLoading) return <main className="min-h-screen bg-slate-50 px-6 pb-16 pt-32" />;
  if (!user) return <main className="min-h-screen bg-slate-50 px-6 pb-16 pt-32"><div className="mx-auto max-w-xl rounded-2xl bg-white p-8 text-center shadow-sm"><h1 className="text-2xl font-bold">Provider tools</h1><p className="mt-2 text-slate-600">Sign in to apply as a landlord or agent.</p><Link href="/login" className="mt-5 inline-block rounded-lg bg-emerald-700 px-5 py-2.5 font-semibold text-white">Sign in</Link></div></main>;

  const latestApplication = applications[0];
  const isApproved = user.provider_status === "approved";

  return <main className="min-h-screen bg-slate-50 px-4 pb-16 pt-28 sm:px-6"><div className="mx-auto max-w-7xl"><p className="text-sm font-semibold uppercase tracking-[0.2em] text-emerald-700">Provider workspace</p><h1 className="mt-2 text-4xl font-bold tracking-tight text-slate-950">Manage your property presence</h1><p className="mt-3 max-w-2xl text-slate-600">Submit trustworthy listings, keep details current, and turn interest into conversations.</p>{message && <p role="status" className="mt-6 rounded-lg bg-emerald-50 p-4 text-emerald-800">{message}</p>}{error && <p role="alert" className="mt-6 rounded-lg bg-red-50 p-4 text-red-800">{error}</p>}{!isApproved ? <div className="mt-8 grid gap-8 lg:grid-cols-[1fr_24rem]"><section className="rounded-2xl bg-white p-6 shadow-sm"><h2 className="text-2xl font-semibold">Become a verified provider</h2><p className="mt-2 text-slate-600">Approved landlords and agents can submit listings for review.</p>{latestApplication && <div className="mt-5 rounded-lg bg-slate-50 p-4 text-sm"><p className="font-semibold">Latest application: <span className="capitalize">{latestApplication.status}</span></p>{latestApplication.review_notes && <p className="mt-1 text-slate-600">{latestApplication.review_notes}</p>}</div>}</section><form onSubmit={submitApplication} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><h2 className="text-xl font-semibold">Apply now</h2><div className="mt-5 space-y-4"><label className="block"><span className="mb-1 block text-sm font-medium">Provider type</span><select value={application.requested_type} onChange={(event) => setApplication({ ...application, requested_type: event.target.value })} className="w-full rounded-lg border border-slate-300 px-3 py-2.5"><option value="landlord">Landlord</option><option value="agent">Agent</option></select></label><label className="block"><span className="mb-1 block text-sm font-medium">Organization or business</span><input value={application.organization_name} onChange={(event) => setApplication({ ...application, organization_name: event.target.value })} className="w-full rounded-lg border border-slate-300 px-3 py-2.5" /></label><label className="block"><span className="mb-1 block text-sm font-medium">Phone</span><input required value={application.phone_number} onChange={(event) => setApplication({ ...application, phone_number: event.target.value })} placeholder="+254…" className="w-full rounded-lg border border-slate-300 px-3 py-2.5" /></label><label className="block"><span className="mb-1 block text-sm font-medium">Tell us about your inventory</span><textarea required minLength={10} value={application.message} onChange={(event) => setApplication({ ...application, message: event.target.value })} rows={4} className="w-full rounded-lg border border-slate-300 px-3 py-2.5" /></label><button disabled={submitting || latestApplication?.status === "pending"} className="w-full rounded-lg bg-emerald-700 px-4 py-3 font-semibold text-white disabled:opacity-60">{latestApplication?.status === "pending" ? "Application under review" : submitting ? "Submitting…" : "Submit application"}</button></div></form></div> : <div className="mt-8 grid gap-8 lg:grid-cols-[24rem_1fr]"><form onSubmit={submitListing} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><h2 className="text-xl font-semibold">Submit a listing</h2><p className="mt-2 text-sm text-slate-600">New and edited listings enter moderation before publication.</p><div className="mt-5 space-y-4"><input required placeholder="Listing title" value={listing.title} onChange={(event) => setListing({ ...listing, title: event.target.value })} className="w-full rounded-lg border border-slate-300 px-3 py-2.5" /><textarea required minLength={20} placeholder="Describe the property" value={listing.description} onChange={(event) => setListing({ ...listing, description: event.target.value })} rows={5} className="w-full rounded-lg border border-slate-300 px-3 py-2.5" /><div className="grid grid-cols-2 gap-3"><select value={listing.listing_type} onChange={(event) => setListing({ ...listing, listing_type: event.target.value })} className="rounded-lg border border-slate-300 px-3 py-2.5"><option value="rent">For rent</option><option value="sale">For sale</option></select><select value={listing.property_type} onChange={(event) => setListing({ ...listing, property_type: event.target.value })} className="rounded-lg border border-slate-300 px-3 py-2.5"><option value="apartment">Apartment</option><option value="house">House</option><option value="townhouse">Townhouse</option><option value="land">Land</option><option value="commercial">Commercial</option></select></div><input required type="number" min="0" placeholder="Price in KES" value={listing.price} onChange={(event) => setListing({ ...listing, price: event.target.value })} className="w-full rounded-lg border border-slate-300 px-3 py-2.5" /><div className="grid grid-cols-2 gap-3"><input required placeholder="City" value={listing.city} onChange={(event) => setListing({ ...listing, city: event.target.value })} className="rounded-lg border border-slate-300 px-3 py-2.5" /><input placeholder="County" value={listing.county} onChange={(event) => setListing({ ...listing, county: event.target.value })} className="rounded-lg border border-slate-300 px-3 py-2.5" /></div><input placeholder="Neighborhood" value={listing.neighborhood} onChange={(event) => setListing({ ...listing, neighborhood: event.target.value })} className="w-full rounded-lg border border-slate-300 px-3 py-2.5" /><input required placeholder="Address" value={listing.address} onChange={(event) => setListing({ ...listing, address: event.target.value })} className="w-full rounded-lg border border-slate-300 px-3 py-2.5" /><div className="grid grid-cols-2 gap-3"><input type="number" min="0" placeholder="Bedrooms" value={listing.bedrooms} onChange={(event) => setListing({ ...listing, bedrooms: event.target.value })} className="rounded-lg border border-slate-300 px-3 py-2.5" /><input type="number" min="0" step="0.5" placeholder="Bathrooms" value={listing.bathrooms} onChange={(event) => setListing({ ...listing, bathrooms: event.target.value })} className="rounded-lg border border-slate-300 px-3 py-2.5" /></div><button disabled={submitting} className="w-full rounded-lg bg-emerald-700 px-4 py-3 font-semibold text-white disabled:opacity-60">{submitting ? "Submitting…" : "Submit for review"}</button></div></form><div className="space-y-8"><section><div className="mb-4 flex items-center justify-between"><h2 className="text-xl font-semibold">Your listings</h2><span className="text-sm text-slate-500">{listings.length} loaded</span></div>{listings.length ? <div className="space-y-4">{listings.map((item) => <article key={item.slug} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><div className="flex flex-wrap items-start justify-between gap-3"><div><h3 className="text-lg font-semibold">{item.title}</h3><p className="mt-1 text-sm text-slate-600">{item.city} · {item.listing_type === "rent" ? "For rent" : "For sale"}</p></div><span className="rounded-full bg-amber-50 px-3 py-1 text-xs font-semibold capitalize text-amber-800">{item.moderation_status.replace("_", " ")}</span></div></article>)}</div> : <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-10 text-center text-slate-600">Your submitted listings will appear here.</div>}</section><section><div className="mb-4 flex items-center justify-between"><h2 className="text-xl font-semibold">Incoming inquiries</h2><span className="text-sm text-slate-500">{inquiries.length} loaded</span></div>{inquiries.length ? <div className="space-y-4">{inquiries.map((inquiry) => <article key={inquiry.id} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><div className="flex flex-wrap items-start justify-between gap-3"><div><h3 className="text-lg font-semibold">{inquiry.property_slug}</h3><p className="mt-1 text-sm text-slate-600">{inquiry.seeker_name} · {inquiry.seeker_email}</p></div><select aria-label={`Status for inquiry ${inquiry.id}`} value={inquiry.status} onChange={(event) => void updateInquiry(inquiry, event.target.value)} className="rounded-lg border border-slate-300 px-3 py-2 text-sm">{inquiryStatuses.map((status) => <option key={status} value={status}>{status}</option>)}</select></div><p className="mt-4 whitespace-pre-wrap text-slate-700">{inquiry.message}</p>{(inquiry.preferred_start || inquiry.preferred_end) && <p className="mt-3 text-sm text-slate-600">Preferred time: {inquiry.preferred_start ?? "—"} to {inquiry.preferred_end ?? "—"}</p>}<textarea aria-label={`Response for inquiry ${inquiry.id}`} value={responses[inquiry.id] ?? inquiry.provider_response} onChange={(event) => setResponses({ ...responses, [inquiry.id]: event.target.value })} rows={3} placeholder="Write a response to the seeker" className="mt-4 w-full rounded-lg border border-slate-300 px-3 py-2.5" /><button type="button" onClick={() => void updateInquiry(inquiry, inquiry.status)} className="mt-3 rounded-lg bg-slate-900 px-4 py-2.5 text-sm font-semibold text-white">Save response</button></article>)}</div> : <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-10 text-center text-slate-600">New inquiries will appear here.</div>}</section></div></div>}</div></main>;
}
