import React, { useState, useEffect } from "react";
import { ServiceCategory, Service } from "@/entities/all";

import HeroSection from "../components/home/HeroSection";
import ServiceCategories from "../components/home/ServiceCategories";
import PopularServices from "../components/home/PopularServices";

export default function Home() {
  const [categories, setCategories] = useState([]);
  const [popularServices, setPopularServices] = useState([]);
  const [isLoadingCategories, setIsLoadingCategories] = useState(true);
  const [isLoadingServices, setIsLoadingServices] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [categoriesData, servicesData] = await Promise.all([
        ServiceCategory.filter({ is_active: true }, "name"),
        Service.filter({ is_popular: true, is_active: true }, "-rating", 6)
      ]);
      
      setCategories(categoriesData);
      setPopularServices(servicesData);
    } catch (error) {
      console.error("Error loading data:", error);
    } finally {
      setIsLoadingCategories(false);
      setIsLoadingServices(false);
    }
  };

  const handleSearch = ({ query, location }) => {
    // Navigate to services page with search params
    window.location.href = `/services?search=${encodeURIComponent(query)}&location=${encodeURIComponent(location)}`;
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <HeroSection onSearchSubmit={handleSearch} />

      {/* Service Categories */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Browse by Category
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Discover our wide range of professional services, all delivered to your home
            </p>
          </div>
          
          <ServiceCategories 
            categories={categories} 
            isLoading={isLoadingCategories}
          />
        </div>
      </section>

      {/* Popular Services */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Most Popular Services
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Book the services loved by thousands of satisfied customers
            </p>
          </div>
          
          <PopularServices 
            services={popularServices}
            isLoading={isLoadingServices}
          />
        </div>
      </section>

      {/* How it Works */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Get premium services in three simple steps
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                step: "1",
                title: "Choose Service",
                description: "Browse and select from our wide range of premium services"
              },
              {
                step: "2", 
                title: "Book Appointment",
                description: "Pick your preferred time and provide your address details"
              },
              {
                step: "3",
                title: "Enjoy Service",
                description: "Our verified professionals arrive at your doorstep on time"
              }
            ].map((item, index) => (
              <div key={index} className="text-center">
                <div className="w-16 h-16 bg-teal-600 rounded-full flex items-center justify-center text-white text-xl font-bold mx-auto mb-4">
                  {item.step}
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">{item.title}</h3>
                <p className="text-gray-600">{item.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}