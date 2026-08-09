"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { ApiError, apiClient } from "../libs/api";
import { useAuth } from "../Pages/API/authCheck";

export default function RegisterPage() {
  const router = useRouter();
  const { refreshAuth } = useAuth();
  const [form, setForm] = useState({ username: "", first_name: "", last_name: "", email: "", password: "", confirmPassword: "" });
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (form.password !== form.confirmPassword) {
      setError("Passwords do not match.");
      return;
    }
    setSubmitting(true);
    setError(null);
    try {
      await apiClient.post("/user/api/v1/auth/register/", { body: { username: form.username, first_name: form.first_name, last_name: form.last_name, email: form.email, password: form.password } });
      await apiClient.post("/user/api/v1/auth/login/", { body: { email: form.email, password: form.password } });
      await refreshAuth();
      router.push("/properties");
    } catch (requestError) {
      setError(requestError instanceof ApiError ? requestError.message : "We could not create your account.");
    } finally {
      setSubmitting(false);
    }
  }

  function update(field: keyof typeof form, value: string) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  return <main className="flex min-h-screen items-center justify-center bg-slate-50 px-4 py-20"><div className="w-full max-w-lg rounded-2xl border border-slate-200 bg-white p-8 shadow-sm"><p className="text-sm font-semibold uppercase tracking-[0.2em] text-emerald-700">Start your search</p><h1 className="mt-2 text-3xl font-bold text-slate-950">Create your Nyumba account</h1><p className="mt-2 text-slate-600">Save properties, contact providers, and request viewings.</p><form onSubmit={submit} className="mt-8 space-y-5"><div className="grid gap-5 sm:grid-cols-2"><label className="block"><span className="mb-1 block text-sm font-medium text-slate-700">First name</span><input required value={form.first_name} onChange={(event) => update("first_name", event.target.value)} className="w-full rounded-lg border border-slate-300 px-3 py-2.5" /></label><label className="block"><span className="mb-1 block text-sm font-medium text-slate-700">Last name</span><input value={form.last_name} onChange={(event) => update("last_name", event.target.value)} className="w-full rounded-lg border border-slate-300 px-3 py-2.5" /></label></div><label className="block"><span className="mb-1 block text-sm font-medium text-slate-700">Username</span><input required autoComplete="username" value={form.username} onChange={(event) => update("username", event.target.value)} className="w-full rounded-lg border border-slate-300 px-3 py-2.5" /></label><label className="block"><span className="mb-1 block text-sm font-medium text-slate-700">Email</span><input required type="email" autoComplete="email" value={form.email} onChange={(event) => update("email", event.target.value)} className="w-full rounded-lg border border-slate-300 px-3 py-2.5" /></label><div className="grid gap-5 sm:grid-cols-2"><label className="block"><span className="mb-1 block text-sm font-medium text-slate-700">Password</span><input required minLength={8} type="password" autoComplete="new-password" value={form.password} onChange={(event) => update("password", event.target.value)} className="w-full rounded-lg border border-slate-300 px-3 py-2.5" /></label><label className="block"><span className="mb-1 block text-sm font-medium text-slate-700">Confirm password</span><input required minLength={8} type="password" autoComplete="new-password" value={form.confirmPassword} onChange={(event) => update("confirmPassword", event.target.value)} className="w-full rounded-lg border border-slate-300 px-3 py-2.5" /></label></div>{error && <p role="alert" className="rounded-lg bg-red-50 p-3 text-sm text-red-800">{error}</p>}<button disabled={submitting} className="w-full rounded-lg bg-emerald-700 px-4 py-3 font-semibold text-white disabled:opacity-60">{submitting ? "Creating account…" : "Create account"}</button></form><p className="mt-6 text-center text-sm text-slate-600">Already registered? <Link href="/login" className="font-semibold text-emerald-700">Sign in</Link></p></div></main>;
}
