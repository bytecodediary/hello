import React from 'react';
import { MapPin, Phone, Mail, Clock } from 'lucide-react';

export default function ContactInfo() {
  return (
    <div className="bg-gray-50 p-8 rounded-lg">
      <h3 className="text-lg font-medium text-gray-900 mb-6">Contact Information</h3>
      <div className="space-y-6">
        <div className="flex items-start">
          <MapPin className="h-6 w-6 text-indigo-600 mt-1" />
          <div className="ml-4">
            <p className="text-sm font-medium text-gray-900">Address</p>
            <p className="text-sm text-gray-600 mt-1">
              123 Business Street<br />
              Suite 100<br />
              New York, NY 10001
            </p>
          </div>
        </div>

        <div className="flex items-start">
          <Phone className="h-6 w-6 text-indigo-600 mt-1" />
          <div className="ml-4">
            <p className="text-sm font-medium text-gray-900">Phone</p>
            <p className="text-sm text-gray-600 mt-1">+1 (555) 123-4567</p>
          </div>
        </div>

        <div className="flex items-start">
          <Mail className="h-6 w-6 text-indigo-600 mt-1" />
          <div className="ml-4">
            <p className="text-sm font-medium text-gray-900">Email</p>
            <p className="text-sm text-gray-600 mt-1">contact@company.com</p>
          </div>
        </div>

        <div className="flex items-start">
          <Clock className="h-6 w-6 text-indigo-600 mt-1" />
          <div className="ml-4">
            <p className="text-sm font-medium text-gray-900">Business Hours</p>
            <p className="text-sm text-gray-600 mt-1">
              Monday - Friday: 9:00 AM - 6:00 PM<br />
              Saturday: 10:00 AM - 4:00 PM<br />
              Sunday: Closed
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}