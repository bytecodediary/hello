'use client';

import React, { useCallback, useEffect, useMemo, useState } from 'react';
import {
  User,
  Home,
  CreditCard,
  Wrench,
  FileText,
  Bell,
  Phone,
  CheckCircle,
  Shield,
  Mail,
  Info,
} from 'lucide-react';
import Header from '@/app/Components/Layouts/Header';
import { apiClient } from '@/app/libs/api';
import type { TenantProfileRecord } from '@/app/type/api';

type ProfileTab =
  | 'personal'
  | 'lease'
  | 'payments'
  | 'maintenance'
  | 'documents'
  | 'preferences'
  | 'emergency';

export default function TenantProfile() {
  const [activeTab, setActiveTab] = useState<ProfileTab>('personal');
  const [profile, setProfile] = useState<TenantProfileRecord | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProfile = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiClient.get<TenantProfileRecord>('/user/profile/tenant/', {
        authenticated: true,
      });
      setProfile(data);
    } catch (err) {
      console.error('Failed to load tenant profile', err);
      setError(err instanceof Error ? err.message : 'Failed to load tenant profile');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void fetchProfile();
  }, [fetchProfile]);

  const tenantName = useMemo(() => {
    if (!profile) return 'Tenant';
    const parts = [profile.user?.first_name, profile.user?.username].filter(Boolean) as string[];
    return parts.join(' ') || 'Tenant';
  }, [profile]);

  const paymentSummaryRows = useMemo(() => {
    if (!profile?.rent_status_summary) {
      return [];
    }

    return [
      {
        id: profile.rent_status_summary.id,
        price: profile.rent_status_summary.price,
        mode: profile.rent_status_summary.payment_mode,
        description: profile.rent_status_summary.description,
        added_at: profile.rent_status_summary.added_at,
        updated_at: profile.rent_status_summary.updated_at,
      },
    ];
  }, [profile]);

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <header className="bg-white shadow-sm py-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-full bg-indigo-100">
                <User className="h-6 w-6 text-indigo-600" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">{tenantName}</h1>
                <p className="text-sm text-gray-500">Tenant Profile</p>
              </div>
            </div>
            {profile?.has_paid && (
              <span className="inline-flex items-center gap-1 rounded-full bg-green-100 px-3 py-1 text-sm font-medium text-green-800">
                <CheckCircle className="h-4 w-4" />
                Payments up to date
              </span>
            )}
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-6 rounded-md border border-destructive bg-destructive/10 p-4 text-destructive">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 gap-8 lg:grid-cols-4">
          <nav className="lg:col-span-1">
            <div className="rounded-lg bg-white p-4 shadow-sm">
              <ul className="space-y-2">
                {[
                  { id: 'personal', icon: User, label: 'Personal Information' },
                  { id: 'lease', icon: Home, label: 'Lease Details' },
                  { id: 'payments', icon: CreditCard, label: 'Payments' },
                  { id: 'maintenance', icon: Wrench, label: 'Maintenance' },
                  { id: 'documents', icon: FileText, label: 'Documents' },
                  { id: 'preferences', icon: Bell, label: 'Preferences' },
                  { id: 'emergency', icon: Phone, label: 'Emergency Contacts' },
                ].map((item) => (
                  <li key={item.id}>
                    <button
                      onClick={() => setActiveTab(item.id as ProfileTab)}
                      className={`flex w-full items-center space-x-3 rounded-md px-4 py-2 text-sm ${
                        activeTab === item.id
                          ? 'bg-indigo-50 text-indigo-600'
                          : 'text-gray-700 hover:bg-gray-50'
                      }`}
                    >
                      <item.icon className="h-5 w-5" />
                      <span>{item.label}</span>
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          </nav>

          <div className="space-y-6 lg:col-span-3">
            {loading ? (
              <div className="rounded-lg bg-white p-6 shadow-sm">
                <div className="h-6 w-1/3 animate-pulse rounded bg-muted" />
                <div className="mt-4 space-y-2">
                  <div className="h-4 w-full animate-pulse rounded bg-muted" />
                  <div className="h-4 w-2/3 animate-pulse rounded bg-muted" />
                  <div className="h-4 w-1/2 animate-pulse rounded bg-muted" />
                </div>
              </div>
            ) : (
              <>
                {activeTab === 'personal' && (
                  <div className="rounded-lg bg-white p-6 shadow-sm">
                    <h2 className="text-xl font-semibold mb-6">Personal Information</h2>
                    <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
                      <div>
                        <label className="block text-sm font-medium text-gray-700">Full Name</label>
                        <p className="mt-1 text-gray-900">{tenantName}</p>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700">Email</label>
                        <p className="mt-1 text-gray-900">{profile?.email ?? '—'}</p>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700">Phone</label>
                        <p className="mt-1 text-gray-900">{profile?.phone_number ?? '—'}</p>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700">Account Status</label>
                        <div className="mt-1 flex items-center space-x-2">
                          <Shield className="h-5 w-5 text-indigo-500" />
                          <span className="text-sm text-gray-700">
                            {profile?.has_paid ? 'Active tenant in good standing' : 'Payment status pending'}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === 'lease' && (
                  <div className="rounded-lg bg-white p-6 shadow-sm">
                    <h2 className="text-xl font-semibold mb-6">Lease Details</h2>
                    <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
                      <div>
                        <label className="block text-sm font-medium text-gray-700">Lease Agreement</label>
                        <p className="mt-1 text-gray-900">{profile?.lease_agreement ?? 'Not provided'}</p>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700">Rent Status</label>
                        <p className="mt-1 text-gray-900">
                          {profile?.rent_status_summary
                            ? `${profile.rent_status_summary.payment_mode} • ${profile.rent_status_summary.price}`
                            : 'No payment information yet'}
                        </p>
                      </div>
                    </div>
                    {profile?.rent_status_summary?.description && (
                      <div className="mt-4 rounded-md bg-muted/40 p-4 text-sm text-muted-foreground">
                        {profile.rent_status_summary.description}
                      </div>
                    )}
                  </div>
                )}

                {activeTab === 'payments' && (
                  <div className="rounded-lg bg-white p-6 shadow-sm">
                    <h2 className="text-xl font-semibold mb-6">Payment Summary</h2>
                    {paymentSummaryRows.length ? (
                      <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-gray-200">
                          <thead>
                            <tr>
                              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Payment ID</th>
                              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Amount</th>
                              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Mode</th>
                              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Created</th>
                              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Updated</th>
                            </tr>
                          </thead>
                          <tbody className="divide-y divide-gray-200">
                            {paymentSummaryRows.map((row) => (
                              <tr key={row.id}>
                                <td className="whitespace-nowrap px-6 py-4 text-sm text-gray-900">{row.id}</td>
                                <td className="whitespace-nowrap px-6 py-4 text-sm text-gray-900">{row.price}</td>
                                <td className="whitespace-nowrap px-6 py-4 text-sm text-gray-900 capitalize">{row.mode}</td>
                                <td className="whitespace-nowrap px-6 py-4 text-sm text-gray-500">
                                  {new Date(row.added_at).toLocaleDateString()}
                                </td>
                                <td className="whitespace-nowrap px-6 py-4 text-sm text-gray-500">
                                  {new Date(row.updated_at).toLocaleDateString()}
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    ) : (
                      <div className="flex items-center gap-2 rounded-md border border-dashed border-muted-foreground/40 bg-muted/20 p-4 text-sm text-muted-foreground">
                        <Info className="h-4 w-4" />
                        No payment records found yet.
                      </div>
                    )}
                  </div>
                )}

                {activeTab === 'maintenance' && (
                  <div className="rounded-lg bg-white p-6 shadow-sm">
                    <div className="mb-6 flex items-center justify-between">
                      <h2 className="text-xl font-semibold">Maintenance Requests</h2>
                      <button className="inline-flex items-center rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700">
                        New Request
                      </button>
                    </div>
                    <div className="rounded-md border border-dashed border-muted-foreground/40 bg-muted/20 p-6 text-center text-sm text-muted-foreground">
                      Maintenance tracking is coming soon.
                    </div>
                  </div>
                )}

                {activeTab === 'documents' && (
                  <div className="rounded-lg bg-white p-6 shadow-sm">
                    <h2 className="text-xl font-semibold mb-6">Documents</h2>
                    {profile?.lease_agreement ? (
                      <div className="flex items-center justify-between rounded-lg border p-4">
                        <div className="flex items-center gap-3">
                          <FileText className="h-5 w-5 text-gray-400" />
                          <div>
                            <p className="text-sm font-medium text-gray-900">Lease Agreement</p>
                            <p className="text-xs text-gray-500">Reference: {profile.lease_agreement}</p>
                          </div>
                        </div>
                        <button className="text-indigo-600 hover:text-indigo-800">
                          View
                        </button>
                      </div>
                    ) : (
                      <div className="rounded-md border border-dashed border-muted-foreground/40 bg-muted/20 p-6 text-center text-sm text-muted-foreground">
                        No documents uploaded yet.
                      </div>
                    )}
                  </div>
                )}

                {activeTab === 'preferences' && (
                  <div className="rounded-lg bg-white p-6 shadow-sm">
                    <h2 className="text-xl font-semibold mb-6">Communication Preferences</h2>
                    <div className="space-y-6">
                      <div>
                        <label className="text-base font-medium text-gray-900">Notification Methods</label>
                        <div className="mt-4 space-y-4">
                          <div className="flex items-center">
                            <input type="checkbox" className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500" defaultChecked />
                            <label className="ml-3 text-sm text-gray-700">Email notifications</label>
                          </div>
                          <div className="flex items-center">
                            <input type="checkbox" className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500" defaultChecked />
                            <label className="ml-3 text-sm text-gray-700">SMS notifications</label>
                          </div>
                          <div className="flex items-center">
                            <input type="checkbox" className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500" />
                            <label className="ml-3 text-sm text-gray-700">Push notifications</label>
                          </div>
                        </div>
                      </div>
                      <div>
                        <label className="text-base font-medium text-gray-900">Notification Types</label>
                        <div className="mt-4 space-y-4">
                          <div className="flex items-center">
                            <input type="checkbox" className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500" defaultChecked />
                            <label className="ml-3 text-sm text-gray-700">Payment reminders</label>
                          </div>
                          <div className="flex items-center">
                            <input type="checkbox" className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500" defaultChecked />
                            <label className="ml-3 text-sm text-gray-700">Maintenance updates</label>
                          </div>
                          <div className="flex items-center">
                            <input type="checkbox" className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500" defaultChecked />
                            <label className="ml-3 text-sm text-gray-700">Building announcements</label>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === 'emergency' && (
                  <div className="rounded-lg bg-white p-6 shadow-sm">
                    <h2 className="text-xl font-semibold mb-6">Emergency Contact Information</h2>
                    <div className="rounded-md border border-dashed border-muted-foreground/40 bg-muted/20 p-6 text-center text-sm text-muted-foreground">
                      Emergency contact details not set yet.
                    </div>
                    <div className="mt-6">
                      <button className="inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50">
                        Update Emergency Contact
                      </button>
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
