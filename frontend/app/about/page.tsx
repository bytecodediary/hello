import Link from "next/link";

export default function AboutPage() {
  return <main className="min-h-screen bg-slate-50 px-6 pb-16 pt-32"><div className="mx-auto max-w-3xl"><p className="text-sm font-semibold uppercase tracking-[0.2em] text-emerald-700">About Nyumba</p><h1 className="mt-3 text-4xl font-bold tracking-tight text-slate-950">Property decisions deserve more clarity.</h1><p className="mt-5 text-lg leading-8 text-slate-600">Nyumba helps people across Kenya discover trusted homes and spaces, connect with providers, and move forward with confidence.</p><div className="mt-8 flex gap-3"><Link href="/properties" className="rounded-lg bg-emerald-700 px-5 py-2.5 font-semibold text-white">Explore properties</Link><Link href="/provider/listings" className="rounded-lg border border-slate-300 px-5 py-2.5 font-semibold text-slate-700">List a property</Link></div></div></main>;
}
