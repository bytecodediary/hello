import { useState } from 'react'
import  { InputSearch }  from "../../Components/ui/Input-search"
import {ButtonSearch }  from "../../Components/ui/Buttonsearch"
import  {Checkbox } from "../../Components/ui/checkbox"
import { ArrowLeft } from "lucide-react"

export default function PropertySearch() {
  const [location, setLocation] = useState('')
  const [propertyType, setPropertyType] = useState('')
  const [priceRange, setPriceRange] = useState('')
  const [bedrooms, setBedrooms] = useState('')

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    // Implement search logic here
    console.log('Searching with:', { location, propertyType, priceRange, bedrooms })
  }

  return (
    <div className="max-w-md mx-auto p-4 bg-white">
      <a href="/" className="flex items-center mb-4">
        <ArrowLeft className="w-6 h-6 mr-2" />
        <h1 className="text-xl font-semibold">Find your property</h1>
      </a>
      <form onSubmit={handleSearch} className="space-y-4">
        <InputSearch
          placeholder="Enter city, state, or ZIP code"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />
        <InputSearch
          placeholder="Property type"
          value={propertyType}
          onChange={(e) => setPropertyType(e.target.value)}
        />
        <InputSearch
          placeholder="Price range"
          value={priceRange}
          onChange={(e) => setPriceRange(e.target.value)}
        />
        <InputSearch
          placeholder="Bedrooms"
          value={bedrooms}
          onChange={(e) => setBedrooms(e.target.value)}
        />
        <ButtonSearch type="submit" className="w-full bg-[#bdb0c7] hover:bg-[#bdb0c9] text-[#0e140e]" label={'Search'}>
          Search
        </ButtonSearch>
      </form>
      <div className="mt-6">
        <h2 className="font-semibold mb-2">Filter by</h2>
        <div className="space-y-2">
          <Checkbox id="budget-friendly" label="Budget-friendly properties" />
          <Checkbox id="breakfast" label="Properties with breakfast included" />
          <Checkbox id="pet-friendly" label="Properties that are pet-friendly" />
          <Checkbox id="instant" label="Instant book" />
        </div>
      </div>
      <div className="mt-4">
        <h2 className="font-semibold mb-2">Price per night</h2>
        <div className="space-y-2">
          <Checkbox id="less-than-50" label="Less than $50 per night" />
          <Checkbox id="50-to-100" label="$50 to $100 per night" />
          <Checkbox id="100-to-200" label="$100 to $200 per night" />
          <Checkbox id="200-plus" label="$200 and more per night" />
        </div>
      </div>
      <div className="mt-4">
        <h2 className="font-semibold mb-2">Property rating</h2>
        <div className="space-y-2">
          <Checkbox id="rating-4" label="4+ rating" />
          <Checkbox id="rating-3" label="3+ rating" />
          <Checkbox id="rating-2" label="2+ rating" />
        </div>
      </div>
    </div>
  )
}