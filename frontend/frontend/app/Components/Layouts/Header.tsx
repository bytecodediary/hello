import Link from "next/link";
import Image from "next/image";
import { TrendingUp, User } from "lucide-react";
import { Button } from "../ui/Button";
import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
import { useAuth } from '../../Pages/API/authCheck';

export default function Header() {
  const { user, logout } = useAuth();

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
          <Link href="/Pages/Search/" className="text-gray-600 hover:text-gray-900">
            Buy
          </Link>
        </li>
        <li>
          <Link href="/Pages/invoices/" className="text-gray-600 hover:text-gray-900">
            Rent
          </Link>
        </li>
        <li>
          <Link href="/real" className="text-gray-600 hover:text-gray-900">
            Sell
          </Link>
        </li>
        <li>
          <Link href="/Pages/profile/" className="text-gray-600 hover:text-gray-900">
            About
          </Link>
         
        </li>
        <li>
          <Link href="/Pages/profile/" className="text-gray-600 hover:text-gray-900">
            Profile
          </Link>
         
        </li>
        <li>
          <Link href="/Pages/propertypage/" className="text-gray-600 hover:text-gray-900">
            Properties
          </Link>
         
        </li>
        <li>
          <Link href="/Pages/contact/" className="text-gray-600 hover:text-gray-900">
            Contact
          </Link>
        </li>
      </ul>

      <div className="flex items-center space-x-4">
        {user ? (
          <>
            {/* Display authenticated user info */}
            <span className="text-sm font-medium text-gray-700">
              Welcome, {user}
            </span>
            <Avatar>
              <AvatarImage src="/path-to-user-avatar" alt={`${user} avatar`} />
              <AvatarFallback>
                <User className="w-5 h-5" />
              </AvatarFallback>
            </Avatar>

            {/* Logout Button */}
            <Button variant="ghost" size="sm" onClick={logout}>
              Log Out
            </Button>
          </>
        ) : (
          <>
            {/* If user is not authenticated, show login/register links */}
            <Button variant="ghost" size="sm" asChild>
              <Link href="/Pages/login/register">New Here?</Link>
            </Button>
            <Button asChild>
              <Link href="/Pages/login/">Log In</Link>
            </Button>
          </>
        )}
      </div>
    </nav>
  );
}
