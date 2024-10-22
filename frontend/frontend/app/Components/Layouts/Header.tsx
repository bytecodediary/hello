import Link from "next/link";
import { TrendingUp } from "lucide-react";
import { Button } from "../ui/Button";

export default function Header() {
  return (
    <nav className="fixed top-0 left-0 right-0 flex items-center justify-between px-4 py-3 bg-white shadow-sm z-50">
      <div className="flex items-center">
        <TrendingUp color="black" className="w-6 h-6 mr-2" />
      </div>
      <ul className="flex space-x-10">
        <li>
          <Link
            href="/Pages/Search/"
            className="text-gray-600 hover:text-gray-900"
          >
            Buy
          </Link>
        </li>
        <li>
          <Link
            href="/Pages/invoices/"
            className="text-gray-600 hover:text-gray-900"
          >
            Rent
          </Link>
        </li>
        <li>
          <Link href="/real" className="text-gray-600 hover:text-gray-900">
            Sell
          </Link>
        </li>
        <li>
          <Link href="/about" className="text-gray-600 hover:text-gray-900">
            About
          </Link>
        </li>
        <li>
          <Link href="/contact" className="text-gray-600 hover:text-gray-900">
            Contact
          </Link>
        </li>
      </ul>
      <div>
        <Button variant="ghost" size="default" href="/Pages/login/register">
          New Here?
        </Button>
        <Link
          href="/Pages/login/"
          className="inline-block px-4 py-2 text-sm font-medium text-white bg-black rounded-full hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
        >
          Join Now
        </Link>
      </div>
    </nav>
  );
}
