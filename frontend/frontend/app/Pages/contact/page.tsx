"use client";

import React from 'react';
import ContactForm from '../contact/contactform';
import ContactInfo from '../contact/contactinfo';

function Contact() {
  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-2xl font-bold text-gray-900">Contact Us</h1>
          <p className="mt-1 text-sm text-gray-500">
            We'd love to hear from you. Send us a message and we'll respond as soon as possible.
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Contact Form */}
          <div className="lg:col-span-2">
            <div className="bg-white shadow-sm rounded-lg p-6 md:p-8">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Send us a Message</h2>
              <ContactForm />
            </div>
          </div>

          {/* Contact Information */}
          <div className="lg:col-span-1">
            <ContactInfo />
          </div>
        </div>
      </main>
    </div>
  );
}

export default Contact;