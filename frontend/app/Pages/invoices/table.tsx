"use client";
import { useCallback, useEffect, useMemo, useState } from 'react';
import { apiClient } from '@/app/libs/api';
import type { OrderRecord } from '@/app/type/api';

interface InvoicesTableProps {
  query: string;
  currentPage: number;
}

export default function InvoicesTable({ query, currentPage }: InvoicesTableProps) {
  const [orders, setOrders] = useState<OrderRecord[]>([]);
  const [totalCount, setTotalCount] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchOrders = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const params: Record<string, string> = { page: String(currentPage) };
      if (query) {
        params.search = query;
      }

      const response = await apiClient.get<OrderRecord[] | { results: OrderRecord[]; count?: number }>(
        '/order',
        {
          authenticated: true,
          query: params,
        }
      );

      const records = Array.isArray(response) ? response : response?.results ?? [];
      const count = Array.isArray(response) ? null : response?.count ?? null;

      setOrders(records);
      setTotalCount(count);
    } catch (err) {
      console.error('Failed to fetch invoices', err);
      setError(err instanceof Error ? err.message : 'Failed to fetch invoices');
      setOrders([]);
      setTotalCount(null);
    } finally {
      setLoading(false);
    }
  }, [currentPage, query]);

  useEffect(() => {
    void fetchOrders();
  }, [fetchOrders]);

  const formattedTotal = useMemo(() => {
    if (totalCount === null) {
      return orders.length;
    }
    return totalCount;
  }, [orders.length, totalCount]);

  if (loading) {
    return (
      <div className="rounded-md border bg-muted/40 p-4 text-sm text-muted-foreground">
        Loading invoices...
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-md border border-destructive bg-destructive/10 p-4 text-destructive">
        {error}
      </div>
    );
  }

  return (
    <div className="rounded-lg border bg-white shadow-sm">
      <div className="flex items-center justify-between px-4 py-3 text-sm text-muted-foreground">
        <span>Showing {orders.length} of {formattedTotal ?? orders.length} invoices</span>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Invoice</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Status</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Total</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Created</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Updated</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 bg-white">
            {orders.length === 0 ? (
              <tr>
                <td colSpan={5} className="px-6 py-8 text-center text-sm text-muted-foreground">
                  No invoices found.
                </td>
              </tr>
            ) : (
              orders.map((order) => (
                <tr key={order.slug}>
                  <td className="whitespace-nowrap px-6 py-4 text-sm font-medium text-gray-900">
                    {order.slug}
                  </td>
                  <td className="whitespace-nowrap px-6 py-4 text-sm text-gray-700 capitalize">
                    {order.status || 'pending'}
                  </td>
                  <td className="whitespace-nowrap px-6 py-4 text-sm text-gray-900">
                    {Intl.NumberFormat('en-KE', {
                      style: 'currency',
                      currency: 'KES',
                      maximumFractionDigits: 0,
                    }).format(order.total)}
                  </td>
                  <td className="whitespace-nowrap px-6 py-4 text-sm text-gray-500">
                    {new Date(order.created_at).toLocaleString()}
                  </td>
                  <td className="whitespace-nowrap px-6 py-4 text-sm text-gray-500">
                    {new Date(order.updated_at).toLocaleString()}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
