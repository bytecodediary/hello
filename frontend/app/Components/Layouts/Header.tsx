"use client";

import Link from "next/link";
import { TrendingUp, User } from "lucide-react";
import { Button } from "../ui/Button";
import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
import { useAuth } from "../../Pages/API/authCheck";

export default function Header() {
  const { user, logout, loading } = useAuth();

  const displayName = user?.username ?? "";

  // if (loading) {
  //   // Display a loader while the authentication status is being fetched
  //   return (
  //     <nav className="fixed top-0 left-0 right-0 flex items-center justify-between px-4 py-3 bg-white shadow-sm z-50">
  //       <div className="flex items-center space-x-2">
  //         <TrendingUp color="black" className="w-6 h-6 mr-2" />
  //         <p>Loading...</p>
  //       </div>
  //     </nav>
  //   );
  // }

  return (
    <nav className="fixed top-0 left-0 right-0 flex items-center justify-between px-4 py-3 bg-white shadow-sm z-50">
       <Link href="/" passHref>
          <div className="flex items-center cursor-pointer">
            <TrendingUp color="black" className="w-6 h-6 mr-2" />
          </div>
      </Link>

      {/* Navigation Links */}
      <ul className="hidden md:flex space-x-10">
        <li>
          <Link href="/properties?listing_type=sale" className="text-gray-600 hover:text-gray-900">
            Buy
          </Link>
        </li>
        <li>
          <Link href="/properties?listing_type=rent" className="text-gray-600 hover:text-gray-900">
            Rent
          </Link>
        </li>
        <li>
          <Link href="/provider/listings" className="text-gray-600 hover:text-gray-900">
            Sell
          </Link>
        </li>
        <li>
          <Link href="/about" className="text-gray-600 hover:text-gray-900">
            About
          </Link>
         
        </li>
        <li>
          <Link href="/account" className="text-gray-600 hover:text-gray-900">
            Profile
          </Link>
         
        </li>
        <li>
          <Link href="/properties" className="text-gray-600 hover:text-gray-900">
            Explore
          </Link>
         
        </li>
        <li>
          <Link href="/Pages/contact/" className="text-gray-600 hover:text-gray-900">
            Contact
          </Link>
        </li>
      </ul>

      <div className="flex items-center space-x-4" suppressHydrationWarning>
        {loading ? (
          <span className="text-sm text-gray-500">Loading account…</span>
        ) : displayName ? (
          <>
            {/* Display authenticated user info */}
            <span className="text-sm font-medium text-gray-700">
              Welcome, {displayName}
            </span>
            <Avatar>
              <AvatarImage src="/path-to-user-avatar" alt={`${displayName} avatar`} />
              <AvatarFallback>
                <User className="w-5 h-5" />
              </AvatarFallback>
            </Avatar>

            {/* Logout Button */}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => logout()}
            >
              Log Out
            </Button>
          </>
        ) : (
          <>
            {/* If user is not authenticated, show login/register links */}
          <Button variant="ghost" size="sm" asChild>
              <Link href="/register">New Here?</Link>
            </Button>
            <Button asChild>
              <Link href="/login">Log In</Link>
            </Button>
          </>
        )}
      </div>
    </nav>
  );
}
