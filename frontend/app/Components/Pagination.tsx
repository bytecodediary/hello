import Link from "next/link";

interface PaginationBarProps {
  currentPage: number;
  totalPages: number;
}

export default function PaginationBar({
  currentPage,
  totalPages,
}: PaginationBarProps) {
  // Calculate the max and min page numbers to display
  const maxPage = Math.min(totalPages, Math.max(currentPage + 4, 10));
  const minPage = Math.max(1, Math.min(currentPage - 5, maxPage - 9));

  const numberedPageItems: JSX.Element[] = [];

  // Loop to create numbered pagination links
  for (let page = minPage; page <= maxPage; page++) {
    numberedPageItems.push(
      <Link
        href={`?page=${page}`}
        key={page}
        className={`join-item btn ${
          currentPage === page ? "btn-active pointer-events-none" : ""
        }`}
      >
        {page}
      </Link>
    );
  }

  return (
    <>
      {/* Desktop pagination: Show number links */}
      <div className="join hidden sm:block">
        {currentPage > 1 && (
          <Link href={`?page=${currentPage - 1}`} className="join-item btn">
            «
          </Link>
        )}
        {numberedPageItems}
        {currentPage < totalPages && (
          <Link href={`?page=${currentPage + 1}`} className="join-item btn">
            »
          </Link>
        )}
      </div>

      {/* Mobile pagination: Show only prev/next and current page info */}
      <div className="join block sm:hidden">
        {currentPage > 1 && (
          <Link href={`?page=${currentPage - 1}`} className="join-item btn">
            «
          </Link>
        )}
        <button className="join-item btn pointer-events-none">
          Page {currentPage} of {totalPages}
        </button>
        {currentPage < totalPages && (
          <Link href={`?page=${currentPage + 1}`} className="join-item btn">
            »
          </Link>
        )}
      </div>
    </>
  );
}
