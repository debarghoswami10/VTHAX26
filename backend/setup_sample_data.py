#!/usr/bin/env python3
"""
Script to set up sample data for the VTHAX26 application
"""

import os
import sys
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Error: SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
    sys.exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_sample_tasks():
    """Create sample tasks"""
    print("Creating sample tasks...")
    
    tasks = [
        {
            "title": "Beauty & Wellness Service",
            "description": "Professional beauty and wellness services including massage, facial, haircare, and spa treatments.",
            "customer_id": "326b68aa-3a5c-45fb-bf31-2dfafb8a4bab"  # Use existing customer ID
        },
        {
            "title": "Home Cleaning Service", 
            "description": "Comprehensive home cleaning services including deep cleaning, kitchen cleaning, and bathroom cleaning.",
            "customer_id": "326b68aa-3a5c-45fb-bf31-2dfafb8a4bab"
        },
        {
            "title": "Repair Services",
            "description": "Professional repair services for plumbing, electrical, furniture, and general home maintenance.",
            "customer_id": "326b68aa-3a5c-45fb-bf31-2dfafb8a4bab"
        },
        {
            "title": "Car Care Services",
            "description": "Complete car care services including car wash, detailing, and maintenance.",
            "customer_id": "326b68aa-3a5c-45fb-bf31-2dfafb8a4bab"
        },
        {
            "title": "Appliance Repair",
            "description": "Professional appliance repair services for home and kitchen appliances.",
            "customer_id": "326b68aa-3a5c-45fb-bf31-2dfafb8a4bab"
        }
    ]
    
    try:
        response = supabase.table("tasks").insert(tasks).execute()
        print(f"✅ Created {len(response.data)} sample tasks")
        return response.data
    except Exception as e:
        print(f"❌ Error creating tasks: {e}")
        return []

def create_sample_taskers():
    """Create sample taskers"""
    print("Creating sample taskers...")
    
    # Create auth users first, then profiles
    tasker_data = [
        {
            "name": "Glow Spa",
            "email": "glow@spa.com",
            "password": "password123",
            "skills": ["Massage", "Facial", "Haircare"],
            "hourly_rate": 75.0,
            "bio": "Professional spa services with 10+ years experience in beauty and wellness."
        },
        {
            "name": "Urban Salon",
            "email": "urban@salon.com",
            "password": "password123",
            "skills": ["Haircut", "Coloring", "Styling"],
            "hourly_rate": 60.0,
            "bio": "Modern salon services specializing in hair cutting and coloring techniques."
        },
        {
            "name": "Clean Pro Services",
            "email": "clean@pro.com",
            "password": "password123",
            "skills": ["Deep Cleaning", "Kitchen Cleaning", "Bathroom Cleaning"],
            "hourly_rate": 45.0,
            "bio": "Professional cleaning services with eco-friendly products and attention to detail."
        },
        {
            "name": "Fix It Right",
            "email": "fix@right.com",
            "password": "password123",
            "skills": ["Plumbing", "Electrical", "General Repairs"],
            "hourly_rate": 80.0,
            "bio": "Licensed repair professionals with expertise in home maintenance and repairs."
        },
        {
            "name": "Auto Care Plus",
            "email": "auto@care.com",
            "password": "password123",
            "skills": ["Car Wash", "Detailing", "Maintenance"],
            "hourly_rate": 50.0,
            "bio": "Complete car care services with professional equipment and quality products."
        }
    ]
    
    created_taskers = []
    
    for tasker in tasker_data:
        try:
            # Create auth user
            user = supabase.auth.sign_up({
                "email": tasker["email"], 
                "password": tasker["password"]
            })
            
            if user.user:
                # Create profile
                profile_data = {
                    "id": user.user.id,
                    "name": tasker["name"],
                    "role": "tasker",
                    "skills": tasker["skills"],
                    "hourly_rate": tasker["hourly_rate"],
                    "bio": tasker["bio"]
                }
                
                response = supabase.table("profiles").insert(profile_data).execute()
                if response.data:
                    created_taskers.extend(response.data)
                    print(f"✅ Created tasker: {tasker['name']}")
                else:
                    print(f"❌ Failed to create profile for: {tasker['name']}")
            else:
                print(f"❌ Failed to create auth user for: {tasker['name']}")
                
        except Exception as e:
            print(f"❌ Error creating tasker {tasker['name']}: {e}")
    
    print(f"✅ Created {len(created_taskers)} sample taskers")
    return created_taskers

def create_sample_bookings():
    """Create sample bookings"""
    print("Creating sample bookings...")
    
    # Get the first task and tasker IDs
    try:
        tasks_response = supabase.table("tasks").select("id").limit(1).execute()
        taskers_response = supabase.table("profiles").select("id").limit(1).execute()
        
        if not tasks_response.data or not taskers_response.data:
            print("❌ No tasks or taskers found. Please create them first.")
            return []
        
        task_id = tasks_response.data[0]["id"]
        tasker_id = taskers_response.data[0]["id"]
        customer_id = "326b68aa-3a5c-45fb-bf31-2dfafb8a4bab"
        
        bookings = [
            {
                "task_id": task_id,
                "tasker_id": tasker_id,
                "customer_id": customer_id,
                "status": "pending"
            },
            {
                "task_id": task_id,
                "tasker_id": tasker_id,
                "customer_id": customer_id,
                "status": "accepted"
            }
        ]
        
        response = supabase.table("bookings").insert(bookings).execute()
        print(f"✅ Created {len(response.data)} sample bookings")
        return response.data
        
    except Exception as e:
        print(f"❌ Error creating bookings: {e}")
        return []

def main():
    """Main function to set up sample data"""
    print("🚀 Setting up sample data for VTHAX26...")
    print("=" * 50)
    
    # Create sample data
    tasks = create_sample_tasks()
    taskers = create_sample_taskers()
    bookings = create_sample_bookings()
    
    print("=" * 50)
    print("✅ Sample data setup complete!")
    print(f"📊 Created: {len(tasks)} tasks, {len(taskers)} taskers, {len(bookings)} bookings")

if __name__ == "__main__":
    main()
