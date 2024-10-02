import Link from "next/link";
import { TrendingUp } from "lucide-react";

export default function Header() {
  return (
    <nav className="flex items-center justify-between px-4 py-3 bg-white shadow-sm">
      <div className="flex items-center">
        <TrendingUp color="black" className="w-6 h-6 mr-2 " />
      </div>
      <ul className="flex space-x-10 ">
        <li>
          <Link href="/Pages/Dashboard/" className="text-gray-600 hover:text-gray-900">
            Buy
          </Link>
        </li>
        <li>
          <Link href="/view" className="text-gray-600 hover:text-gray-900">
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
      <button className="px-4 py-2 text-sm font-medium text-white bg-black rounded-full hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500">
        Join Now
      </button>
    </nav>
  );
}
