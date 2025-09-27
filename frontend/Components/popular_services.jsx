import React from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Star, Clock, TrendingUp } from "lucide-react";
import { Link } from "react-router-dom";
import { createPageUrl } from "@/utils";

export default function PopularServices({ services, isLoading }) {
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {Array(6).fill(0).map((_, i) => (
          <Card key={i} className="animate-pulse">
            <div className="h-48 bg-gray-200"></div>
            <CardContent className="p-4">
              <div className="h-4 bg-gray-200 rounded mb-2"></div>
              <div className="h-3 bg-gray-200 rounded mb-4 w-3/4"></div>
              <div className="flex justify-between items-center">
                <div className="h-4 bg-gray-200 rounded w-16"></div>
                <div className="h-8 bg-gray-200 rounded w-20"></div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {services.map((service) => (
        <Card key={service.id} className="group hover:shadow-xl transition-all duration-300 cursor-pointer border-0 shadow-md overflow-hidden">
          <div className="relative">
            <img
              src={service.image_url || `https://images.unsplash.com/photo-1560472354-b33ff0c44a43?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80`}
              alt={service.name}
              className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
            />
            {service.is_popular && (
              <Badge className="absolute top-3 left-3 bg-orange-500 text-white border-0">
                <TrendingUp className="w-3 h-3 mr-1" />
                Popular
              </Badge>
            )}
            <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent"></div>
          </div>
          
          <CardContent className="p-4">
            <div className="flex items-start justify-between mb-2">
              <h3 className="font-bold text-lg text-gray-900 group-hover:text-teal-600 transition-colors">
                {service.name}
              </h3>
              <div className="flex items-center space-x-1 text-sm text-amber-600">
                <Star className="w-4 h-4 fill-current" />
                <span className="font-medium">{service.rating || '4.8'}</span>
              </div>
            </div>
            
            <p className="text-sm text-gray-600 mb-3 line-clamp-2">
              {service.short_description || service.description}
            </p>
            
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="text-lg font-bold text-teal-600">
                  ₹{service.price}
                </div>
                {service.duration && (
                  <div className="flex items-center text-sm text-gray-500">
                    <Clock className="w-4 h-4 mr-1" />
                    {service.duration}m
                  </div>
                )}
              </div>
              
              <Link to={createPageUrl(`ServiceDetails?id=${service.id}`)}>
                <Button 
                  size="sm" 
                  className="bg-teal-600 hover:bg-teal-700 text-white rounded-full px-6"
                >
                  Book Now
                </Button>
              </Link>
            </div>
            
            {service.total_bookings > 0 && (
              <div className="mt-3 text-xs text-gray-500">
                {service.total_bookings} people booked this service
              </div>
            )}
          </CardContent>
        </Card>
      ))}
    </div>
  );
}