import React from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Link } from "react-router-dom";
import { createPageUrl } from "@/utils";
import * as Icons from "lucide-react";

export default function ServiceCategories({ categories, isLoading }) {
  if (isLoading) {
    return (
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        {Array(12).fill(0).map((_, i) => (
          <Card key={i} className="animate-pulse">
            <CardContent className="p-6 text-center">
              <div className="w-12 h-12 bg-gray-200 rounded-full mx-auto mb-3"></div>
              <div className="h-4 bg-gray-200 rounded mx-auto"></div>
            </CardContent>
          </Card>
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
      {categories.map((category) => {
        const IconComponent = Icons[category.icon] || Icons.Wrench;
        
        return (
          <Link
            key={category.id}
            to={createPageUrl(`Services?category=${category.id}`)}
            className="group"
          >
            <Card className="hover:shadow-lg transition-all duration-300 group-hover:-translate-y-1 cursor-pointer border-0 shadow-md">
              <CardContent className="p-6 text-center">
                <div 
                  className="w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3 group-hover:scale-110 transition-transform duration-300"
                  style={{ backgroundColor: `${category.color}20` }}
                >
                  <IconComponent 
                    className="w-6 h-6" 
                    style={{ color: category.color || '#0F766E' }}
                  />
                </div>
                <h3 className="font-semibold text-sm text-gray-900 group-hover:text-teal-600 transition-colors">
                  {category.name}
                </h3>
              </CardContent>
            </Card>
          </Link>
        );
      })}
    </div>
  );
}