#!/usr/bin/env python3
"""
Script to fix booking data integrity issues:
1. Update bookings with null customer_id to have proper customer IDs
2. Ensure proper data isolation between users
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Missing SUPABASE_URL or SUPABASE_KEY environment variables")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fix_bookings_data():
    """Fix booking data integrity issues"""
    print("🔧 Starting booking data cleanup...")
    
    try:
        # Get all bookings with null customer_id
        response = supabase.table("bookings").select("*").is_("customer_id", "null").execute()
        null_customer_bookings = response.data or []
        
        print(f"📊 Found {len(null_customer_bookings)} bookings with null customer_id")
        
        if not null_customer_bookings:
            print("✅ No bookings with null customer_id found")
            return
        
        # Get all customer profiles
        customers_response = supabase.table("profiles").select("id, name").eq("role", "customer").execute()
        customers = customers_response.data or []
        
        print(f"👥 Found {len(customers)} customers in database")
        
        if not customers:
            print("❌ No customers found in database")
            return
        
        # Assign bookings to customers (round-robin assignment)
        for i, booking in enumerate(null_customer_bookings):
            customer = customers[i % len(customers)]
            
            # Update the booking with the customer ID
            update_response = supabase.table("bookings").update({
                "customer_id": customer["id"]
            }).eq("id", booking["id"]).execute()
            
            if update_response.data:
                print(f"✅ Updated booking {booking['id']} -> Customer: {customer['name']} ({customer['id']})")
            else:
                print(f"❌ Failed to update booking {booking['id']}")
        
        print("🎉 Booking data cleanup completed!")
        
        # Verify the fix
        verify_fix()
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")

def verify_fix():
    """Verify that the fix worked"""
    print("\n🔍 Verifying fix...")
    
    try:
        # Check for remaining null customer_id bookings
        response = supabase.table("bookings").select("id, customer_id").is_("customer_id", "null").execute()
        remaining_null = response.data or []
        
        if remaining_null:
            print(f"⚠️  Still {len(remaining_null)} bookings with null customer_id")
        else:
            print("✅ All bookings now have proper customer_id")
        
        # Show booking distribution by customer
        customers_response = supabase.table("profiles").select("id, name").eq("role", "customer").execute()
        customers = customers_response.data or []
        
        print("\n📊 Booking distribution by customer:")
        for customer in customers:
            bookings_response = supabase.table("bookings").select("id").eq("customer_id", customer["id"]).execute()
            booking_count = len(bookings_response.data or [])
            print(f"  {customer['name']}: {booking_count} bookings")
            
    except Exception as e:
        print(f"❌ Error during verification: {e}")

def create_sample_bookings():
    """Create sample bookings for testing if needed"""
    print("\n🎯 Creating sample bookings for testing...")
    
    try:
        # Get a customer and tasker
        customers_response = supabase.table("profiles").select("id").eq("role", "customer").limit(1).execute()
        taskers_response = supabase.table("profiles").select("id").eq("role", "tasker").limit(1).execute()
        
        if not customers_response.data or not taskers_response.data:
            print("❌ Need at least one customer and one tasker to create sample bookings")
            return
        
        customer_id = customers_response.data[0]["id"]
        tasker_id = taskers_response.data[0]["id"]
        
        # Get a task
        tasks_response = supabase.table("tasks").select("id").limit(1).execute()
        if not tasks_response.data:
            print("❌ No tasks found in database")
            return
        
        task_id = tasks_response.data[0]["id"]
        
        # Create sample bookings
        sample_bookings = [
            {
                "task_id": task_id,
                "customer_id": customer_id,
                "tasker_id": tasker_id,
                "status": "pending"
            },
            {
                "task_id": task_id,
                "customer_id": customer_id,
                "tasker_id": tasker_id,
                "status": "accepted"
            }
        ]
        
        for booking in sample_bookings:
            response = supabase.table("bookings").insert(booking).execute()
            if response.data:
                print(f"✅ Created sample booking: {booking['status']}")
            else:
                print(f"❌ Failed to create sample booking: {booking['status']}")
                
    except Exception as e:
        print(f"❌ Error creating sample bookings: {e}")

if __name__ == "__main__":
    print("🚀 Booking Data Cleanup Tool")
    print("=" * 40)
    
    # Fix existing data
    fix_bookings_data()
    
    # Create sample data automatically
    print("\n" + "=" * 40)
    create_sample_bookings()
    
    print("\n🎉 All done!")
