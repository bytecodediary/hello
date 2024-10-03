"use client";

import { useEffect, useState } from 'react';
import Header from "@/app/Components/Layouts/Header";
import CardProperties from "@/app/Components/ui/Cardproperties";
import PropertySearch from "./Property-search";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/app/Components/ui/select";

export default function Buy() {
  const [fix, setFix] = useState(false);

  const setFixedSidebar = () => {
    const scrollY = window.scrollY;
    if (scrollY >= 150 && !fix) {
      setFix(true);
    } else if (scrollY < 150 && fix) {
      setFix(false);
    }
  };
  

  useEffect(() => {
    window.addEventListener('scroll', setFixedSidebar);
    return () => {
      window.removeEventListener('scroll', setFixedSidebar);
    };
  }, []);

  return (
    <div>
      <Header />
      <section>
      <div className="flex flex-grow border-2 max-h-full  ">
        <div className={`w-1/3 p-4 border-2 shadow-lg ${fix ? ' fixed  h-screen' : 'sidebar'}`}>
          <PropertySearch />
        </div>
        <div className={`w-2/3 p-4 border-2 shadow-lg ${fix ? 'ml-[33.33%]' : ''}`}>
          <div className="bg-[#f8faf8] p-4 rounded-lg">
            <div className="flex justify-between items-center">
              <div>
                <p className="text-sm text-gray-600 mb-1">
                  1126 search results for
                </p>
                <h1 className="text-2xl font-bold">Properties in Nakuru</h1>
              </div>
              <div>
                <Select>
                  <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder="Sort by" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="price-asc">
                      Price: Low to High
                    </SelectItem>
                    <SelectItem value="price-desc">
                      Price: High to Low
                    </SelectItem>
                    <SelectItem value="rating">Rating</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </div>
          <CardProperties />
        </div>a
      </div>
      </section>
      {/* <Footer /> */}
    </div>
  );
}
