"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { ApiError, apiClient } from "../libs/api";
import { useAuth } from "../Pages/API/authCheck";

export default function LoginPage() {
  const router = useRouter();
  const { refreshAuth } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      await apiClient.post("/user/api/v1/auth/login/", { body: { email, password } });
      await refreshAuth();
      router.push("/properties");
    } catch (requestError) {
      setError(requestError instanceof ApiError ? requestError.message : "We could not sign you in.");
    } finally {
      setSubmitting(false);
    }
  }

  return <main className="flex min-h-screen items-center justify-center bg-slate-50 px-4 py-20"><div className="w-full max-w-md rounded-2xl border border-slate-200 bg-white p-8 shadow-sm"><p className="text-sm font-semibold uppercase tracking-[0.2em] text-emerald-700">Welcome back</p><h1 className="mt-2 text-3xl font-bold text-slate-950">Sign in to Nyumba</h1><p className="mt-2 text-slate-600">Continue your search and manage your enquiries.</p><form onSubmit={submit} className="mt-8 space-y-5"><label className="block"><span className="mb-1 block text-sm font-medium text-slate-700">Email</span><input required type="email" autoComplete="email" value={email} onChange={(event) => setEmail(event.target.value)} className="w-full rounded-lg border border-slate-300 px-3 py-2.5" /></label><label className="block"><span className="mb-1 block text-sm font-medium text-slate-700">Password</span><input required type="password" autoComplete="current-password" value={password} onChange={(event) => setPassword(event.target.value)} className="w-full rounded-lg border border-slate-300 px-3 py-2.5" /></label>{error && <p role="alert" className="rounded-lg bg-red-50 p-3 text-sm text-red-800">{error}</p>}<button disabled={submitting} className="w-full rounded-lg bg-emerald-700 px-4 py-3 font-semibold text-white disabled:opacity-60">{submitting ? "Signing in…" : "Sign in"}</button></form><p className="mt-6 text-center text-sm text-slate-600">New to Nyumba? <Link href="/register" className="font-semibold text-emerald-700">Create an account</Link></p></div></main>;
}
