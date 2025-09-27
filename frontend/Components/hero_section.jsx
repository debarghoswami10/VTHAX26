import React from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Search, MapPin, Star } from "lucide-react";

export default function HeroSection({ onSearchSubmit }) {
  const [searchQuery, setSearchQuery] = React.useState("");
  const [location, setLocation] = React.useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearchSubmit({ query: searchQuery, location });
  };

  return (
    <div className="relative bg-gradient-to-r from-teal-600 to-teal-800 overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 bg-black opacity-20"></div>
      <div className="absolute inset-0" style={{
        backgroundImage: "url('https://images.unsplash.com/photo-1560472354-b33ff0c44a43?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1926&q=80')",
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        opacity: 0.3
      }}></div>
      
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24">
        <div className="text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-white mb-6 leading-tight">
            Premium Services
            <span className="block text-teal-200">At Your Doorstep</span>
          </h1>
          <p className="text-xl text-teal-100 mb-8 max-w-2xl mx-auto">
            Book trusted professionals for beauty, wellness, repairs, and more. 
            All services delivered to your home with guaranteed satisfaction.
          </p>

          {/* Search Form */}
          <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
            <div className="bg-white rounded-2xl shadow-2xl p-4 md:p-6">
              <div className="grid grid-cols-1 md:grid-cols-12 gap-4">
                <div className="md:col-span-5">
                  <div className="relative">
                    <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <Input
                      placeholder="What service do you need?"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="pl-12 h-14 text-lg border-0 focus:ring-2 focus:ring-teal-500 rounded-xl"
                    />
                  </div>
                </div>
                <div className="md:col-span-5">
                  <div className="relative">
                    <MapPin className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <Input
                      placeholder="Your location"
                      value={location}
                      onChange={(e) => setLocation(e.target.value)}
                      className="pl-12 h-14 text-lg border-0 focus:ring-2 focus:ring-teal-500 rounded-xl"
                    />
                  </div>
                </div>
                <div className="md:col-span-2">
                  <Button 
                    type="submit" 
                    className="w-full h-14 bg-teal-600 hover:bg-teal-700 text-white font-semibold rounded-xl text-lg shadow-lg hover:shadow-xl transition-all duration-300"
                  >
                    Search
                  </Button>
                </div>
              </div>
            </div>
          </form>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-12 max-w-2xl mx-auto">
            <div className="text-center">
              <div className="flex items-center justify-center mb-2">
                <Star className="w-5 h-5 text-teal-200 mr-1" />
                <span className="text-2xl font-bold text-white">4.8</span>
              </div>
              <p className="text-teal-200">Average Rating</p>
            </div>
            <div className="text-center">
              <h3 className="text-2xl font-bold text-white mb-2">50K+</h3>
              <p className="text-teal-200">Happy Customers</p>
            </div>
            <div className="text-center">
              <h3 className="text-2xl font-bold text-white mb-2">1000+</h3>
              <p className="text-teal-200">Verified Professionals</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}