"use client";

import Image from "next/image";
import Header from "./Components/Layouts/Header";
import Heroimg from "./Public/Image/herohouse.png";
import Homeservice from "./Components/ui/Homeservice";
import { ChevronDown } from "lucide-react";
import "./style/Homeservice.css";
import { Button } from "@/app/Components/ui/Button";
import Footer from "./Components/Layouts/Footer";

export default function Home() {
  return (
    <div>
      <Header />
      <section className="container mx-auto pl-10 py-12 flex items-center justify-between">
        <div className="flex px-4 items-center">
          <div className="hero-left flex-1">
            <h2 className="text-5xl font-bold leading-tight mb-4 text-black ">
              Timberline Heights: Your gateway platform for
            </h2>
            <p className="text-xl text-gray-600 mb-8">
              Timberline Heights is a user-friendly platform for property
              solutions, connecting customers and stakeholders.
            </p>
            <div className="flex space-x-4">
              <Button variant="primary" size="lg">
                Start exploring
              </Button>
              <Button variant="secondary" size="lg">
                List property
              </Button>
            </div>
          </div>
          <div className="hero-right flex-1">
            <Image
              src={Heroimg}
              alt="Colorful house illustration"
              width={400}
              height={400}
              className="object-contain"
            />
          </div>
        </div>
      </section>
      <div className="container mx-auto px-4 py-12 items-center justify-between">
        <ChevronDown className="mx-auto mb-8 w-6 h-6 text-black" />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10 pl-10">
          <StatItem
            title="Your Property Portfolio"
            value="$802,906,041"
            className="text-3xl md:text-4xl font-bold text-black"
          />
          <StatItem
            title="Current Property Value"
            value="7,366%"
            className="text-3xl md:text-4xl font-bold text-black"
          />
          <StatItem
            title="Total Properties Listed"
            value="Over $3 billion"
            className="text-3xl md:text-4xl font-bold text-black"
          />
          <StatItem
            title="% Properties Listed"
            value="90.4%"
            className="text-3xl md:text-4xl font-bold text-black"
          />
        </div>
      </div>
      <Homeservice />

      <Footer />
    </div>
  );
}

interface StatItemProps {
  title: string;
  value: string;
  className: string;
}

function StatItem({ title, value, className }: StatItemProps) {
  return (
    <div className="space-y-2">
      <h3 className="text-lg font-medium text-black">{title}</h3>
      <p className={className}>{value}</p>
    </div>
  );
}
