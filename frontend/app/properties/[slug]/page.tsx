"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";

import PropertyDetails from "../../Components/property/PropertyDetails";
import type { PropertyRecord } from "../../type/api";
import { ApiError, apiClient } from "../../libs/api";
import { useAuth } from "../../Pages/API/authCheck";

function InquiryForm({ property }: { property: PropertyRecord }) {
  const { user } = useAuth();
  const [type, setType] = useState("inquiry");
  const [message, setMessage] = useState("");
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");
  const [state, setState] = useState<"idle" | "sending" | "sent">("idle");
  const [error, setError] = useState<string | null>(null);

  if (!user) return <div className="rounded-2xl bg-slate-900 p-6 text-white"><h2 className="text-xl font-semibold">Interested in this property?</h2><p className="mt-2 text-slate-300">Sign in to contact the provider or request a viewing.</p><Link href="/login" className="mt-5 inline-block rounded-lg bg-emerald-400 px-4 py-2.5 font-semibold text-slate-950">Sign in to enquire</Link></div>;

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setState("sending");
    setError(null);
    try {
      await apiClient.post(`/api/v1/listings/${encodeURIComponent(property.slug)}/inquiries/`, {
        body: {
          inquiry_type: type,
          message,
          ...(type === "viewing" && start ? { preferred_start: new Date(start).toISOString() } : {}),
          ...(type === "viewing" && end ? { preferred_end: new Date(end).toISOString() } : {}),
        },
      });
      setState("sent");
      setMessage("");
    } catch (requestError) {
      setState("idle");
      setError(requestError instanceof ApiError ? requestError.message : "Your request could not be sent.");
    }
  }

  return <form onSubmit={submit} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><h2 className="text-xl font-semibold text-slate-950">Contact the provider</h2><p className="mt-2 text-sm text-slate-600">Ask a question or suggest a time for a viewing.</p><div className="mt-5 space-y-4"><label className="block"><span className="mb-1 block text-sm font-medium text-slate-700">Request type</span><select value={type} onChange={(event) => setType(event.target.value)} className="w-full rounded-lg border border-slate-300 px-3 py-2.5"><option value="inquiry">Ask a question</option><option value="viewing">Request a viewing</option></select></label>{type === "viewing" && <div className="grid gap-4 sm:grid-cols-2"><label className="block"><span className="mb-1 block text-sm font-medium text-slate-700">Preferred start</span><input required type="datetime-local" value={start} onChange={(event) => setStart(event.target.value)} className="w-full rounded-lg border border-slate-300 px-3 py-2.5" /></label><label className="block"><span className="mb-1 block text-sm font-medium text-slate-700">Preferred end</span><input type="datetime-local" value={end} onChange={(event) => setEnd(event.target.value)} className="w-full rounded-lg border border-slate-300 px-3 py-2.5" /></label></div>}<label className="block"><span className="mb-1 block text-sm font-medium text-slate-700">Message</span><textarea required minLength={10} maxLength={2000} rows={5} value={message} onChange={(event) => setMessage(event.target.value)} placeholder="Tell the provider what you would like to know…" className="w-full rounded-lg border border-slate-300 px-3 py-2.5" /></label>{error && <p role="alert" className="text-sm text-red-700">{error}</p>}{state === "sent" && <p role="status" className="text-sm font-medium text-emerald-700">Request sent. The provider will get back to you.</p>}<button disabled={state === "sending"} className="w-full rounded-lg bg-emerald-700 px-4 py-3 font-semibold text-white disabled:opacity-60">{state === "sending" ? "Sending…" : "Send request"}</button></div></form>;
}

export default function PropertyPage() {
  const params = useParams<{ slug: string }>();
  const router = useRouter();
  const { user } = useAuth();
  const [property, setProperty] = useState<PropertyRecord | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    apiClient.get<PropertyRecord>(`/api/v1/listings/${encodeURIComponent(params.slug)}/`, { authenticated: false })
      .then(setProperty)
      .catch((requestError) => setError(requestError instanceof ApiError ? requestError.message : "Property could not be loaded."))
      .finally(() => setLoading(false));
  }, [params.slug]);

  async function toggleSaved() {
    if (!property || !user) return;
    try {
      if (saved) {
        await apiClient.delete(`/api/v1/listings/${encodeURIComponent(property.slug)}/favorite/`);
        setSaved(false);
      } else {
        await apiClient.post(`/api/v1/listings/${encodeURIComponent(property.slug)}/favorite/`);
        setSaved(true);
      }
    } catch (requestError) {
      setError(requestError instanceof ApiError ? requestError.message : "The saved property could not be updated.");
    }
  }

  if (loading) return <main className="min-h-screen bg-slate-50 px-6 pb-16 pt-32"><div className="mx-auto max-w-6xl animate-pulse"><div className="h-[30rem] rounded-2xl bg-slate-200" /></div></main>;
  if (error || !property) return <main className="min-h-screen bg-slate-50 px-6 pb-16 pt-32"><div className="mx-auto max-w-2xl rounded-2xl border border-red-200 bg-red-50 p-8 text-red-800">{error ?? "Property not found."}</div></main>;

  return <main className="min-h-screen bg-slate-50 px-4 pb-16 pt-28 sm:px-6"><div className="mx-auto max-w-6xl"><div className="mb-5 flex items-center justify-between"><button onClick={() => router.back()} className="text-sm font-semibold text-slate-600 hover:text-slate-950">← Back to properties</button>{user && <button onClick={toggleSaved} className="rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50">{saved ? "Saved" : "Save property"}</button>}</div><PropertyDetails property={property} onBack={() => router.back()} /><div className="mt-8 grid gap-8 lg:grid-cols-[1fr_24rem]"><div className="rounded-2xl bg-emerald-50 p-6"><h2 className="text-xl font-semibold text-slate-950">A clearer way to move</h2><p className="mt-2 text-slate-700">Ask questions, request a viewing, and keep your property search in one place.</p></div><InquiryForm property={property} /></div></div></main>;
}
