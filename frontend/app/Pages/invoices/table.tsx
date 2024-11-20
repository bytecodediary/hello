"use client";
import { useEffect, useState } from 'react';

interface Invoice {
  id: number;
  amount: number;
  date: string;
}

interface InvoicesTableProps {
  query: string;
  currentPage: number;
}

export default function InvoicesTable({ query, currentPage }: InvoicesTableProps) {
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchInvoices = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await fetchFilteredInvoices(query, currentPage);
        setInvoices(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch invoices');
      } finally {
        setLoading(false);
      }
    };

    fetchInvoices();
  }, [query, currentPage]);

  if (loading) {
    return <div>Loading...</div>; // Consider a spinner here
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Amount</th>
          <th>Date</th>
          {/* Add more headers as necessary */}
        </tr>
      </thead>
      <tbody>
        {invoices.length === 0 ? (
          <tr>
            <td colSpan={3}>No invoices found.</td>
          </tr>
        ) : (
          invoices.map((invoice) => (
            <tr key={invoice.id}>
              <td>{invoice.id}</td>
              <td>{invoice.amount}</td>
              <td>{new Date(invoice.date).toLocaleDateString()}</td> {/* Format the date */}
              {/* Render more invoice data as needed */}
            </tr>
          ))
        )}
      </tbody>
    </table>
  );
}

async function fetchFilteredInvoices(query: string, currentPage: number): Promise<Invoice[]> {
  // Implement the API call to fetch invoices based on query and page
  throw new Error('Function not implemented.');
}
