'use client';

import React, { useState } from 'react';
import {
  User, Home, CreditCard, Wrench, FileText, Bell, Phone,
  CheckCircle, Calendar, Clock, ChevronRight, Shield, Mail
} from 'lucide-react';

export default function TenantProfile() {
  const [activeTab, setActiveTab] = useState('personal');

  const tenant = {
    name: "Sarah Anderson",
    email: "sarah.anderson@email.com",
    phone: "(555) 123-4567",
    verified: true,
    lease: {
      address: "123 Modern Apartments, Unit 4B",
      startDate: "2023-08-01",
      endDate: "2024-07-31",
      monthlyRent: 2200
    },
    paymentHistory: [
      { date: "2024-03-01", amount: 2200, status: "Paid" },
      { date: "2024-02-01", amount: 2200, status: "Paid" },
      { date: "2024-01-01", amount: 2200, status: "Paid" }
    ],
    maintenanceRequests: [
      { id: "MR-001", date: "2024-02-28", issue: "Dishwasher repair", status: "In Progress" },
      { id: "MR-002", date: "2024-01-15", issue: "HVAC maintenance", status: "Completed" }
    ],
    documents: [
      { name: "Lease Agreement 2023-2024", date: "2023-07-25" },
      { name: "Renter's Insurance Policy", date: "2023-07-28" },
      { name: "Move-in Inspection Report", date: "2023-08-01" }
    ],
    emergency: {
      name: "Michael Anderson",
      relation: "Brother",
      phone: "(555) 987-6543"
    }
  };

  return (

    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="h-12 w-12 rounded-full bg-indigo-100 flex items-center justify-center">
                <User className="h-6 w-6 text-indigo-600" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">{tenant.name}</h1>
                <p className="text-sm text-gray-500">Tenant Profile</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              {tenant.verified && (
                <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                  <CheckCircle className="h-4 w-4 mr-1" /> Verified
                </span>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar Navigation */}
          <nav className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-sm p-4">
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
                      onClick={() => setActiveTab(item.id)}
                      className={`w-full flex items-center space-x-3 px-4 py-2 rounded-md text-sm ${
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

          {/* Main Content Area */}
          <div className="lg:col-span-3 space-y-6">
            {/* Personal Information Section */}
            {activeTab === 'personal' && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h2 className="text-xl font-semibold mb-6">Personal Information</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Full Name</label>
                    <p className="mt-1 text-gray-900">{tenant.name}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Email</label>
                    <p className="mt-1 text-gray-900">{tenant.email}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Phone</label>
                    <p className="mt-1 text-gray-900">{tenant.phone}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">ID Verification</label>
                    <div className="mt-1 flex items-center space-x-2">
                      <Shield className="h-5 w-5 text-green-500" />
                      <span className="text-green-600">Verified</span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Lease Details Section */}
            {activeTab === 'lease' && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h2 className="text-xl font-semibold mb-6">Current Lease Details</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Property Address</label>
                    <p className="mt-1 text-gray-900">{tenant.lease.address}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Monthly Rent</label>
                    <p className="mt-1 text-gray-900">${tenant.lease.monthlyRent}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Lease Start Date</label>
                    <p className="mt-1 text-gray-900">{new Date(tenant.lease.startDate).toLocaleDateString()}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Lease End Date</label>
                    <p className="mt-1 text-gray-900">{new Date(tenant.lease.endDate).toLocaleDateString()}</p>
                  </div>
                </div>
              </div>
            )}

             {/* Payments Section */}
             {activeTab === 'payments' && (
              <div className="space-y-6">
                <div className="bg-white rounded-lg shadow-sm p-6">
                  <h2 className="text-xl font-semibold mb-6">Payment History</h2>
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead>
                        <tr>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-200">
                        {tenant.paymentHistory.map((payment, index) => (
                          <tr key={index}>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                              {new Date(payment.date).toLocaleDateString()}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                              ${payment.amount}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                {payment.status}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            )}

            {/* Maintenance Section */}
            {activeTab === 'maintenance' && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-xl font-semibold">Maintenance Requests</h2>
                  <button className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700">
                    New Request
                  </button>
                </div>
                <div className="space-y-4">
                  {tenant.maintenanceRequests.map((request) => (
                    <div key={request.id} className="border rounded-lg p-4">
                      <div className="flex justify-between items-start">
                        <div>
                          <h3 className="text-lg font-medium text-gray-900">{request.issue}</h3>
                          <p className="text-sm text-gray-500">Request ID: {request.id}</p>
                          <p className="text-sm text-gray-500">
                            Submitted: {new Date(request.date).toLocaleDateString()}
                          </p>
                        </div>
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          request.status === 'Completed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                        }`}>
                          {request.status}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Documents Section */}
            {activeTab === 'documents' && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h2 className="text-xl font-semibold mb-6">Documents</h2>
                <div className="space-y-4">
                  {tenant.documents.map((doc, index) => (
                    <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center space-x-3">
                        <FileText className="h-5 w-5 text-gray-400" />
                        <div>
                          <p className="text-sm font-medium text-gray-900">{doc.name}</p>
                          <p className="text-xs text-gray-500">
                            Added: {new Date(doc.date).toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                      <button className="text-indigo-600 hover:text-indigo-800">
                        <ChevronRight className="h-5 w-5" />
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Preferences Section */}
            {activeTab === 'preferences' && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h2 className="text-xl font-semibold mb-6">Communication Preferences</h2>
                <div className="space-y-6">
                  <div>
                    <label className="text-base font-medium text-gray-900">Notification Methods</label>
                    <div className="mt-4 space-y-4">
                      <div className="flex items-center">
                        <input type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" defaultChecked />
                        <label className="ml-3 text-sm text-gray-700">Email notifications</label>
                      </div>
                      <div className="flex items-center">
                        <input type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" defaultChecked />
                        <label className="ml-3 text-sm text-gray-700">SMS notifications</label>
                      </div>
                      <div className="flex items-center">
                        <input type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" />
                        <label className="ml-3 text-sm text-gray-700">Push notifications</label>
                      </div>
                    </div>
                  </div>
                  <div>
                    <label className="text-base font-medium text-gray-900">Notification Types</label>
                    <div className="mt-4 space-y-4">
                      <div className="flex items-center">
                        <input type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" defaultChecked />
                        <label className="ml-3 text-sm text-gray-700">Payment reminders</label>
                      </div>
                      <div className="flex items-center">
                        <input type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" defaultChecked />
                        <label className="ml-3 text-sm text-gray-700">Maintenance updates</label>
                      </div>
                      <div className="flex items-center">
                        <input type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" defaultChecked />
                        <label className="ml-3 text-sm text-gray-700">Building announcements</label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

              {/* Emergency Contacts Section */}
              {activeTab === 'emergency' && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h2 className="text-xl font-semibold mb-6">Emergency Contact Information</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Contact Name</label>
                    <p className="mt-1 text-gray-900">{tenant.emergency.name}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Relationship</label>
                    <p className="mt-1 text-gray-900">{tenant.emergency.relation}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Phone Number</label>
                    <p className="mt-1 text-gray-900">{tenant.emergency.phone}</p>
                  </div>
                </div>
                <div className="mt-6">
                  <button className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                    Update Emergency Contact
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
