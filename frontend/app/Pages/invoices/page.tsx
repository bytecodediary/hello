// import Pagination from '@/app/ui/invoices/pagination';
import Search from '@/app/Components/ui/search';
import Table from '@/app/Pages/invoices/table';
// import { CreateInvoice } from '@/app/ui/invoices/buttons';
// import { InvoicesTableSkeleton } from '@/app/ui/skeletons';
import { Suspense } from 'react';

export default async function Page({
    searchParams,
}: {
    searchParams?: {
        query?: string;
        page?: string;
    };
}) {
    const query = searchParams?.query || '';
    const currentPage = Number(searchParams?.page) || 1; // Use 1 instead of '1'
    
    return (
        <div className="w-full">
            <div className="flex w-full items-center justify-between">
                <h1>Invoices</h1>
            </div>
            <div className="mt-4 flex items-center justify-between gap-2 md:mt-8">
                <Search />

            </div>
            <Suspense key={query + currentPage} >
                <Table query={query} currentPage={currentPage} />
            </Suspense>
            <div className="mt-5 flex w-full justify-center">
                {/* Uncomment when ready */}
                {/* <Pagination totalPages={totalPages} /> */}
            </div>
        </div>
    );
}
