import { InputSearch } from "../../Components/ui/Input-search";
import { ButtonSearch } from "../../Components/ui/Buttonsearch";
import { Checkbox } from "../../Components/ui/checkbox";
import { ArrowLeft } from "lucide-react";

interface PropertySearchProps {
  location: string;
  onLocationChange: (value: string) => void;
  onSubmit: () => void;
  loading?: boolean;
}

export default function PropertySearch({
  location,
  onLocationChange,
  onSubmit,
  loading = false,
}: PropertySearchProps) {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit();
  };

  return (
    <div className="sidebar max-w-md mx-auto p-4 bg-white">
      <a href="/" className="flex items-center mb-4">
        <ArrowLeft className="w-6 h-6 mr-2" />
        <h1 className="text-xl font-semibold">Find your property</h1>
      </a>
      <form onSubmit={handleSubmit} className="space-y-4">
        <InputSearch
          placeholder="Enter city, state, or ZIP code"
          value={location}
          onChange={(e) => onLocationChange(e.target.value)}
        />
        <ButtonSearch
          type="submit"
          className="w-full bg-[#bdb0c7] hover:bg-[#bdb0c9] text-[#0e140e]"
          label={loading ? "Searching..." : "Search"}
          disabled={loading}
        >
          {loading ? "Searching..." : "Search"}
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
        <p className="mt-2 text-xs text-muted-foreground">
          Additional filters coming soon.
        </p>
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
  );
}
