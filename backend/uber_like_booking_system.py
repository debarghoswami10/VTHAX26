#!/usr/bin/env python3
"""
Uber-like Booking System Implementation
This module provides enhanced booking functionality similar to Uber/Uber Eats
"""

import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from supabase import create_client, Client

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Error: SUPABASE_URL and SUPABASE_KEY environment variables are required")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class UberLikeBookingSystem:
    """Uber-like booking system with real-time status tracking and management"""
    
    def __init__(self):
        self.status_transitions = {
            'pending': ['accepted', 'declined', 'cancelled'],
            'accepted': ['in-progress', 'cancelled'],
            'in-progress': ['completed', 'cancelled'],
            'completed': [],
            'declined': [],
            'cancelled': []
        }
    
    def create_booking(self, customer_id: str, tasker_id: str, task_id: int, 
                      service_name: str = None, special_instructions: str = None) -> Dict:
        """Create a new booking (like placing an Uber order)"""
        try:
            # Get customer details
            customer = supabase.table("profiles").select("name, phone, address").eq("id", customer_id).execute()
            customer_data = customer.data[0] if customer.data else {}
            
            # Get tasker details
            tasker = supabase.table("profiles").select("name, phone, hourly_rate").eq("id", tasker_id).execute()
            tasker_data = tasker.data[0] if tasker.data else {}
            
            # Get task details
            task = supabase.table("tasks").select("title, description, estimated_price").eq("id", task_id).execute()
            task_data = task.data[0] if task.data else {}
            
            # Create booking with Uber-like structure
            booking_data = {
                "task_id": task_id,
                "customer_id": customer_id,
                "tasker_id": tasker_id,
                "status": "pending",
                "created_at": datetime.now().isoformat(),
                # Store additional details in a JSON field or separate table
                "service_name": service_name or task_data.get("title", "Service"),
                "customer_name": customer_data.get("name", "Customer"),
                "customer_phone": customer_data.get("phone", ""),
                "customer_address": customer_data.get("address", ""),
                "provider_name": tasker_data.get("name", "Provider"),
                "provider_phone": tasker_data.get("phone", ""),
                "estimated_price": tasker_data.get("hourly_rate", 0),
                "special_instructions": special_instructions or ""
            }
            
            # Insert booking
            response = supabase.table("bookings").insert(booking_data).execute()
            
            if response.data:
                return {
                    "success": True,
                    "booking_id": response.data[0]["id"],
                    "status": "pending",
                    "message": "Booking created successfully! Waiting for provider to accept..."
                }
            else:
                return {"success": False, "message": "Failed to create booking"}
                
        except Exception as e:
            return {"success": False, "message": f"Error creating booking: {str(e)}"}
    
    def get_customer_bookings(self, customer_id: str) -> List[Dict]:
        """Get all bookings for a customer (like Uber customer app)"""
        try:
            response = supabase.table("bookings") \
                .select("""
                    id, task_id, customer_id, tasker_id, status, created_at,
                    task:tasks(title, description),
                    tasker:profiles!bookings_tasker_id_fkey(name, phone, rating)
                """) \
                .eq("customer_id", customer_id) \
                .order("created_at", desc=True) \
                .execute()
            
            bookings = []
            for booking in response.data or []:
                booking_info = {
                    "id": booking["id"],
                    "status": booking["status"],
                    "created_at": booking["created_at"],
                    "service_name": booking.get("task", {}).get("title", "Service"),
                    "service_description": booking.get("task", {}).get("description", ""),
                    "provider_name": booking.get("tasker", {}).get("name", "Provider"),
                    "provider_phone": booking.get("tasker", {}).get("phone", ""),
                    "provider_rating": booking.get("tasker", {}).get("rating", 0),
                    "status_display": self._get_status_display(booking["status"]),
                    "can_cancel": booking["status"] in ["pending", "accepted"],
                    "can_rate": booking["status"] == "completed"
                }
                bookings.append(booking_info)
            
            return bookings
            
        except Exception as e:
            print(f"Error fetching customer bookings: {e}")
            return []
    
    def get_provider_bookings(self, provider_id: str) -> List[Dict]:
        """Get all bookings for a provider (like Uber driver app)"""
        try:
            response = supabase.table("bookings") \
                .select("""
                    id, task_id, customer_id, tasker_id, status, created_at,
                    task:tasks(title, description),
                    customer:profiles!bookings_customer_id_fkey(name, phone, address)
                """) \
                .eq("tasker_id", provider_id) \
                .order("created_at", desc=True) \
                .execute()
            
            bookings = []
            for booking in response.data or []:
                booking_info = {
                    "id": booking["id"],
                    "status": booking["status"],
                    "created_at": booking["created_at"],
                    "service_name": booking.get("task", {}).get("title", "Service"),
                    "service_description": booking.get("task", {}).get("description", ""),
                    "customer_name": booking.get("customer", {}).get("name", "Customer"),
                    "customer_phone": booking.get("customer", {}).get("phone", ""),
                    "customer_address": booking.get("customer", {}).get("address", ""),
                    "status_display": self._get_status_display(booking["status"]),
                    "can_accept": booking["status"] == "pending",
                    "can_start": booking["status"] == "accepted",
                    "can_complete": booking["status"] == "in-progress",
                    "can_decline": booking["status"] == "pending"
                }
                bookings.append(booking_info)
            
            return bookings
            
        except Exception as e:
            print(f"Error fetching provider bookings: {e}")
            return []
    
    def update_booking_status(self, booking_id: int, new_status: str, user_id: str) -> Dict:
        """Update booking status (like Uber status updates)"""
        try:
            # Get current booking
            booking = supabase.table("bookings").select("*").eq("id", booking_id).execute()
            if not booking.data:
                return {"success": False, "message": "Booking not found"}
            
            current_booking = booking.data[0]
            current_status = current_booking["status"]
            
            # Check if transition is valid
            if new_status not in self.status_transitions.get(current_status, []):
                return {
                    "success": False, 
                    "message": f"Cannot change status from {current_status} to {new_status}"
                }
            
            # Prepare update data
            update_data = {"status": new_status}
            
            # Add timestamp based on status
            now = datetime.now().isoformat()
            if new_status == "accepted":
                update_data["accepted_at"] = now
            elif new_status == "in-progress":
                update_data["started_at"] = now
            elif new_status == "completed":
                update_data["completed_at"] = now
            elif new_status == "cancelled":
                update_data["cancelled_at"] = now
            
            # Update booking
            response = supabase.table("bookings") \
                .update(update_data) \
                .eq("id", booking_id) \
                .execute()
            
            if response.data:
                return {
                    "success": True,
                    "message": f"Booking status updated to {self._get_status_display(new_status)}",
                    "new_status": new_status
                }
            else:
                return {"success": False, "message": "Failed to update booking status"}
                
        except Exception as e:
            return {"success": False, "message": f"Error updating booking: {str(e)}"}
    
    def get_available_providers(self, service_category: str = None) -> List[Dict]:
        """Get available providers (like Uber driver matching)"""
        try:
            query = supabase.table("profiles") \
                .select("id, name, skills, hourly_rate, rating, bio") \
                .eq("role", "tasker") \
                .eq("is_available", True)
            
            if service_category:
                query = query.contains("skills", [service_category])
            
            response = query.order("rating", desc=True).execute()
            
            providers = []
            for provider in response.data or []:
                provider_info = {
                    "id": provider["id"],
                    "name": provider["name"],
                    "skills": provider.get("skills", []),
                    "hourly_rate": provider.get("hourly_rate", 0),
                    "rating": provider.get("rating", 0),
                    "bio": provider.get("bio", ""),
                    "is_available": True
                }
                providers.append(provider_info)
            
            return providers
            
        except Exception as e:
            print(f"Error fetching providers: {e}")
            return []
    
    def get_booking_statistics(self, user_id: str, user_role: str) -> Dict:
        """Get booking statistics (like Uber dashboard stats)"""
        try:
            if user_role == "customer":
                bookings = self.get_customer_bookings(user_id)
            else:
                bookings = self.get_provider_bookings(user_id)
            
            stats = {
                "total_bookings": len(bookings),
                "pending": len([b for b in bookings if b["status"] == "pending"]),
                "accepted": len([b for b in bookings if b["status"] == "accepted"]),
                "in_progress": len([b for b in bookings if b["status"] == "in-progress"]),
                "completed": len([b for b in bookings if b["status"] == "completed"]),
                "cancelled": len([b for b in bookings if b["status"] == "cancelled"])
            }
            
            return stats
            
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {}
    
    def _get_status_display(self, status: str) -> str:
        """Get user-friendly status display"""
        status_map = {
            "pending": "Waiting for Provider",
            "accepted": "Provider Accepted",
            "in-progress": "Service in Progress",
            "completed": "Service Completed",
            "cancelled": "Cancelled",
            "declined": "Declined by Provider"
        }
        return status_map.get(status, status.title())
    
    def search_bookings(self, user_id: str, user_role: str, query: str) -> List[Dict]:
        """Search bookings (like Uber search functionality)"""
        try:
            if user_role == "customer":
                bookings = self.get_customer_bookings(user_id)
            else:
                bookings = self.get_provider_bookings(user_id)
            
            # Simple text search
            query_lower = query.lower()
            filtered_bookings = []
            
            for booking in bookings:
                if (query_lower in booking.get("service_name", "").lower() or
                    query_lower in booking.get("service_description", "").lower() or
                    query_lower in booking.get("provider_name", "").lower() or
                    query_lower in booking.get("customer_name", "").lower()):
                    filtered_bookings.append(booking)
            
            return filtered_bookings
            
        except Exception as e:
            print(f"Error searching bookings: {e}")
            return []

# Example usage and testing
if __name__ == "__main__":
    booking_system = UberLikeBookingSystem()
    
    print("🚀 Uber-like Booking System")
    print("=" * 50)
    
    # Test creating a booking
    print("\n📝 Testing booking creation...")
    result = booking_system.create_booking(
        customer_id="test-customer-id",
        tasker_id="test-tasker-id", 
        task_id=1,
        service_name="Home Cleaning",
        special_instructions="Please use eco-friendly products"
    )
    print(f"Result: {result}")
    
    print("\n✅ Uber-like booking system is ready!")
    print("Features implemented:")
    print("• Real-time booking creation")
    print("• Status tracking and updates")
    print("• Customer and provider dashboards")
    print("• Search and filtering")
    print("• Statistics and analytics")
    print("• Uber-like user experience")
