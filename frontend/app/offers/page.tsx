"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { ApiError, apiClient } from "../libs/api";
import { useAuth } from "../Pages/API/authCheck";
import type { PaginatedResponse, PaymentIntentRecord, PropertyOfferRecord } from "../type/api";

export default function OffersPage() {
  const { user, loading: authLoading } = useAuth();
  const [offers, setOffers] = useState<PropertyOfferRecord[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [paymentPhones, setPaymentPhones] = useState<Record<number, string>>({});
  const [paymentStatuses, setPaymentStatuses] = useState<Record<number, PaymentIntentRecord["status"]>>({});
  const [payingOfferId, setPayingOfferId] = useState<number | null>(null);

  async function withdrawOffer(offer: PropertyOfferRecord) {
    try {
      const updated = await apiClient.patch<PropertyOfferRecord>(`/api/v1/account/offers/${offer.id}/withdraw/`, { body: {} });
      setOffers((current) => current.map((item) => (item.id === updated.id ? updated : item)));
    } catch (requestError) {
      setError(requestError instanceof ApiError ? requestError.message : "The offer could not be withdrawn.");
    }
  }

  async function startPayment(offer: PropertyOfferRecord) {
    const phoneNumber = paymentPhones[offer.id]?.trim();
    if (!phoneNumber) {
      setError("Enter the M-Pesa phone number to continue.");
      return;
    }

    try {
      setPayingOfferId(offer.id);
      setError(null);
      const intent = await apiClient.post<PaymentIntentRecord>("/payment/intents/", {
        body: { offer: offer.id, phone_number: phoneNumber },
        headers: { "Idempotency-Key": crypto.randomUUID() },
      });
      setPaymentStatuses((current) => ({ ...current, [offer.id]: intent.status }));
    } catch (requestError) {
      setError(requestError instanceof ApiError ? requestError.message : "The payment could not be started.");
    } finally {
      setPayingOfferId(null);
    }
  }

  useEffect(() => {
    if (!user) return;
    apiClient.get<PaginatedResponse<PropertyOfferRecord>>("/api/v1/account/offers/")
      .then((response) => setOffers(response.results))
      .catch((requestError) => setError(requestError instanceof ApiError ? requestError.message : "Offers could not be loaded."));
  }, [user]);

  if (authLoading) return <main className="min-h-screen bg-slate-50 px-6 pb-16 pt-32" />;
  if (!user) return <main className="min-h-screen bg-slate-50 px-6 pb-16 pt-32"><div className="mx-auto max-w-xl rounded-2xl bg-white p-8 text-center shadow-sm"><h1 className="text-2xl font-bold text-slate-950">Your offers</h1><p className="mt-2 text-slate-600">Sign in to track offers and reservation requests.</p><Link href="/login" className="mt-5 inline-block rounded-lg bg-emerald-700 px-5 py-2.5 font-semibold text-white">Sign in</Link></div></main>;

  return <main className="min-h-screen bg-slate-50 px-4 pb-16 pt-28 sm:px-6"><div className="mx-auto max-w-4xl"><p className="text-sm font-semibold uppercase tracking-[0.2em] text-emerald-700">Your account</p><h1 className="mt-2 text-4xl font-bold tracking-tight text-slate-950">Offers and reservation requests</h1><p className="mt-3 text-slate-600">Keep track of the conversations that could become your next move.</p>{error && <p role="alert" className="mt-6 rounded-lg bg-red-50 p-4 text-red-800">{error}</p>}{offers.length ? <div className="mt-8 space-y-4">{offers.map((offer) => <article key={offer.id} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><div className="flex flex-wrap items-start justify-between gap-3"><div><Link href={`/properties/${encodeURIComponent(offer.property_slug)}`} className="text-lg font-semibold text-slate-950 hover:text-emerald-700">{offer.property_slug}</Link><p className="mt-1 text-sm capitalize text-slate-600">{offer.offer_type} · {offer.currency} {Number(offer.amount).toLocaleString()}</p></div><span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold capitalize text-slate-700">{offer.status}</span></div>{offer.message && <p className="mt-4 whitespace-pre-wrap text-slate-700">{offer.message}</p>}{offer.provider_response && <div className="mt-4 rounded-lg bg-emerald-50 p-4 text-sm text-emerald-900"><p className="font-semibold">Provider response</p><p className="mt-1 whitespace-pre-wrap">{offer.provider_response}</p></div>}{offer.expires_at && <p className="mt-4 text-xs text-slate-500">Expires {new Date(offer.expires_at).toLocaleString()}</p>}{offer.status === "submitted" && <button type="button" onClick={() => void withdrawOffer(offer)} className="mt-4 rounded-lg border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700">Withdraw request</button>}{offer.status === "accepted" && <form onSubmit={(event) => { event.preventDefault(); void startPayment(offer); }} className="mt-5 rounded-xl border border-emerald-100 bg-emerald-50/60 p-4"><p className="font-semibold text-emerald-950">Secure the agreement</p><p className="mt-1 text-sm text-emerald-900">Start an M-Pesa payment for the accepted offer. The payment is only marked successful after the provider callback.</p><label className="mt-4 block"><span className="mb-1 block text-sm font-medium text-emerald-950">M-Pesa phone number</span><input required inputMode="tel" autoComplete="tel" value={paymentPhones[offer.id] ?? ""} onChange={(event) => setPaymentPhones((current) => ({ ...current, [offer.id]: event.target.value }))} placeholder="0712 345 678" className="w-full rounded-lg border border-emerald-200 bg-white px-3 py-2.5" /></label><button type="submit" disabled={payingOfferId === offer.id} className="mt-3 rounded-lg bg-emerald-700 px-4 py-2.5 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60">{payingOfferId === offer.id ? "Starting payment…" : `Pay ${offer.currency} ${Number(offer.amount).toLocaleString()} via M-Pesa`}</button>{paymentStatuses[offer.id] && <p role="status" className="mt-3 text-sm font-medium capitalize text-emerald-900">Payment status: {paymentStatuses[offer.id]}</p>}</form>}</article>)}</div> : <div className="mt-8 rounded-2xl border border-dashed border-slate-300 bg-white p-12 text-center"><h2 className="text-xl font-semibold">No offers yet</h2><p className="mt-2 text-slate-600">When you are ready, open a property and submit an offer or reservation request.</p><Link href="/properties" className="mt-5 inline-block rounded-lg bg-emerald-700 px-5 py-2.5 font-semibold text-white">Explore properties</Link></div>}</div></main>;
}
