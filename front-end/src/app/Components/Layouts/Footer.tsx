import {
  Facebook,
  Twitter,
  Instagram,
  Linkedin,
  Mail,
  Phone,
} from "lucide-react";
import Input from "../../Components/ui/Input";
import Image from "next/image";
import Link from "next/link";
import { Button } from "../../Components/ui/Button";
import Footerimg from "../../Public/Image/footerimg.png";
import "./footer.css";

export default function Footer() {
  return (
    <footer className=" relative flex flex-row	">
      <div className=" topper rounded-lg mb-8 flex flex-col md:flex-row items-center absolute">
        <Image
          src={Footerimg}
          alt="Tinted house with a blue roof over a cyliner"
          width={400}
          height={400}
          className="mb-4 md:mb-0 md:mr-8"
        />
        <div className="text-white text-center md:textF-left">
          <h2 className="text-2xl font-bold mb-2">
            Subscribe to our newsletter to get updates to our latest collections
          </h2>
          <p className="mb-4">
            Get 20% off on your first order just by subscribing to our
            newsletter
          </p>
          <form className="flex flex-col sm:flex-row gap-2">
            <Input
              type="email"
              placeholder="Enter your email"
              className="bg-white text-black"
              required
            />
            <Button variant="primary" size="lg">
              Email us
            </Button>
          </form>
          <p className="text-sm mt-2">
            You will be able to unsubscribe at any time. Read our privacy policy
            here.
          </p>
        </div>
      </div>
      <div className=" lower container mx-auto px-4 py-8 bg-white ">
        <div className="grid grid-cols-1 md:grid-cols-5 gap-8">
          <div className="col-span-1 md:col-span-2">
            <p className="text-black mb-4">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit ut
              aliquam, purus sit amet luctus venenatis.
            </p>
            <div className="flex space-x-4">
              <Link href="#" className="text-gray-400 hover:text-gray-500">
                <Facebook size={24} />
              </Link>
              <Link href="#" className="text-gray-400 hover:text-gray-500">
                <Twitter size={24} />
              </Link>
              <Link href="#" className="text-gray-400 hover:text-gray-500">
                <Instagram size={24} />
              </Link>
              <Link href="#" className="text-gray-400 hover:text-gray-500">
                <Linkedin size={24} />
              </Link>
            </div>
          </div>

          <div>
            <h3 className="font-bold mb-4 text-black">Company</h3>
            <ul className="space-y-2">
              <li>
                <Link href="#" className="text-gray-600 hover:text-gray-800">
                  About Us
                </Link>
              </li>
              <li>
                <Link href="#" className="text-gray-600 hover:text-gray-800">
                  Services
                </Link>
              </li>
              <li>
                <Link href="#" className="text-gray-600 hover:text-gray-800">
                  Community
                </Link>
              </li>
              <li>
                <Link href="#" className="text-gray-600 hover:text-gray-800">
                  Testimonial
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="font-bold mb-4 text-black">Support</h3>
            <ul className="space-y-2">
              <li>
                <Link href="#" className="text-gray-600 hover:text-gray-800">
                  Help Center
                </Link>
              </li>
              <li>
                <Link href="#" className="text-gray-600 hover:text-gray-800">
                  X @ Us
                </Link>
              </li>
              <li>
                <Link href="#" className="text-gray-600 hover:text-gray-800">
                  Webinars
                </Link>
              </li>
              <li>
                <Link href="#" className="text-gray-600 hover:text-gray-800">
                  Feedback
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="font-bold mb-4 text-black">Links</h3>
            <ul className="space-y-2">
              <li>
                <Link href="#" className="text-gray-600 hover:text-gray-800">
                  Courses
                </Link>
              </li>
              <li>
                <Link href="#" className="text-gray-600 hover:text-gray-800">
                  Become Teacher
                </Link>
              </li>
              <li>
                <Link href="#" className="text-gray-600 hover:text-gray-800">
                  Service
                </Link>
              </li>
              <li>
                <Link href="#" className="text-gray-600 hover:text-gray-800">
                  All in One
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="font-bold mb-4 text-black">Contact Us</h3>
            <ul className="space-y-2">
              <li className="flex items-center">
                <Phone size={18} className="mr-2 text-gray-400" />
                <span className="text-gray-600">(91) 98765 4321 54</span>
              </li>
              <li className="flex items-center">
                <Mail size={18} className="mr-2 text-gray-400" />
                <a
                  href="mailto:support@mail.com"
                  className="text-gray-600 hover:text-gray-800"
                >
                  support@mail.com
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t mt-8 pt-8 flex flex-col sm:flex-row justify-between items-center">
          <p className="text-gray-600 text-sm mb-4 sm:mb-0">
            © Copyright by Codedui. All rights reserved.
          </p>
          <div className="flex space-x-4">
            <Link
              href="#"
              className="text-gray-600 hover:text-gray-800 text-sm"
            >
              Privacy Policy
            </Link>
            <Link
              href="#"
              className="text-gray-600 hover:text-gray-800 text-sm"
            >
              Terms of Use
            </Link>
            <Link
              href="#"
              className="text-gray-600 hover:text-gray-800 text-sm"
            >
              Legal
            </Link>
            <Link
              href="#"
              className="text-gray-600 hover:text-gray-800 text-sm"
            >
              Site Map
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
