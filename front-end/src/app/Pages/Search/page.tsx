"use client";
import Header from "@/app/Components/Layouts/Header";
import Footer from "@/app/Components/Layouts/Footer";
import CardProperties from "@/app/Components/ui/Cardproperties";
import PropertySearch from "./Property-search";

export default function Buy() {
  return (
    <div>
      <Header />
      <div className="flex">
        <div className="w-1/3 p-4">
         <PropertySearch /> 
        </div>
        <div className="w-2/3 p-4">
          <CardProperties />
        </div>
      </div>
      <Footer />
    </div>
  );
}
