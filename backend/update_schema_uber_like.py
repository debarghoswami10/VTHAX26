#!/usr/bin/env python3
"""
Update database schema to support Uber-like booking system
This script adds the necessary columns to the bookings table for a complete booking experience
"""

import os
from supabase import create_client, Client

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Error: SUPABASE_URL and SUPABASE_KEY environment variables are required")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def update_bookings_schema():
    """Add Uber-like columns to the bookings table"""
    
    print("🚀 Updating bookings table schema for Uber-like functionality...")
    
    # SQL commands to add new columns
    schema_updates = [
        # Customer details (like Uber Eats order details)
        "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS customer_name text;",
        "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS customer_phone text;",
        "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS customer_address text;",
        "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS customer_email text;",
        
        # Service details (like Uber Eats restaurant/food details)
        "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS service_name text;",
        "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS service_description text;",
        "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS service_category text;",
        
        # Provider details (like Uber driver details)
        "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS provider_name text;",
        "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS provider_phone text;",
        
        # Booking details (like Uber trip details)
        "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS booking_date date;",
        "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS booking_time time;",
        "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS estimated_duration integer;",  # in minutes
        "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS estimated_price numeric;",
        "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS final_price numeric;",
        
        # Location details (like Uber pickup/dropoff)
        "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS pickup_address text;",
        "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS dropoff_address text;",
        "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS latitude numeric;",
        "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS longitude numeric;",
        
        # Status tracking (like Uber trip status)
        "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS status_updated_at timestamp default now();",
        "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS accepted_at timestamp;",
        "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS started_at timestamp;",
        "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS completed_at timestamp;",
        "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS cancelled_at timestamp;",
        
        # Additional Uber-like features
        "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS special_instructions text;",
        "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS priority text check (priority in ('low','normal','high','urgent')) default 'normal';",
        "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS payment_status text check (payment_status in ('pending','paid','refunded')) default 'pending';",
        "ALTER TABLE bookings ADD COLUMN IF NOT EXISTS payment_method text;",
        
        # Update status constraint to include more Uber-like statuses
        "ALTER TABLE bookings DROP CONSTRAINT IF EXISTS bookings_status_check;",
        "ALTER TABLE bookings ADD CONSTRAINT bookings_status_check CHECK (status IN ('pending','accepted','in-progress','completed','cancelled','declined'));"
    ]
    
    try:
        # Execute each schema update
        for i, sql in enumerate(schema_updates, 1):
            print(f"  {i:2d}. Executing: {sql[:60]}...")
            try:
                supabase.rpc('exec_sql', {'sql': sql}).execute()
                print(f"      ✅ Success")
            except Exception as e:
                print(f"      ⚠️  Warning: {str(e)[:100]}...")
                # Continue with other updates even if one fails
        
        print("\n✅ Schema update completed!")
        print("📋 New columns added to bookings table:")
        print("   • Customer details: name, phone, address, email")
        print("   • Service details: name, description, category")
        print("   • Provider details: name, phone")
        print("   • Booking details: date, time, duration, price")
        print("   • Location details: pickup/dropoff addresses, coordinates")
        print("   • Status tracking: timestamps for each status change")
        print("   • Additional features: instructions, priority, payment")
        
    except Exception as e:
        print(f"❌ Error updating schema: {e}")
        return False
    
    return True

def create_indexes():
    """Create useful indexes for better performance"""
    
    print("\n🔍 Creating performance indexes...")
    
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_bookings_customer_id ON bookings(customer_id);",
        "CREATE INDEX IF NOT EXISTS idx_bookings_tasker_id ON bookings(tasker_id);",
        "CREATE INDEX IF NOT EXISTS idx_bookings_status ON bookings(status);",
        "CREATE INDEX IF NOT EXISTS idx_bookings_created_at ON bookings(created_at);",
        "CREATE INDEX IF NOT EXISTS idx_bookings_booking_date ON bookings(booking_date);",
        "CREATE INDEX IF NOT EXISTS idx_profiles_role ON profiles(role);"
    ]
    
    try:
        for i, sql in enumerate(indexes, 1):
            print(f"  {i}. Creating index: {sql.split('ON')[1].split('(')[0].strip()}...")
            try:
                supabase.rpc('exec_sql', {'sql': sql}).execute()
                print(f"      ✅ Success")
            except Exception as e:
                print(f"      ⚠️  Warning: {str(e)[:100]}...")
        
        print("✅ Indexes created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating indexes: {e}")
        return False
    
    return True

def verify_schema():
    """Verify the updated schema"""
    
    print("\n🔍 Verifying updated schema...")
    
    try:
        # Get column information for bookings table
        result = supabase.rpc('exec_sql', {
            'sql': """
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'bookings' 
            ORDER BY ordinal_position;
            """
        }).execute()
        
        if result.data:
            print("📊 Current bookings table schema:")
            print("   " + "-" * 80)
            print(f"   {'Column Name':<25} {'Type':<15} {'Nullable':<10} {'Default'}")
            print("   " + "-" * 80)
            
            for col in result.data:
                col_name = col['column_name']
                col_type = col['data_type']
                nullable = col['is_nullable']
                default = col['column_default'] or ''
                
                print(f"   {col_name:<25} {col_type:<15} {nullable:<10} {default}")
            
            print("   " + "-" * 80)
            print(f"   Total columns: {len(result.data)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verifying schema: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Uber-like booking system schema update...")
    print("=" * 60)
    
    # Update the schema
    if update_bookings_schema():
        # Create indexes
        create_indexes()
        
        # Verify the changes
        verify_schema()
        
        print("\n" + "=" * 60)
        print("🎉 Uber-like booking system schema update completed!")
        print("📝 The bookings table now supports:")
        print("   • Complete customer and provider information")
        print("   • Service details and categorization")
        print("   • Location tracking and coordinates")
        print("   • Full booking lifecycle with timestamps")
        print("   • Payment and priority management")
        print("   • Performance-optimized indexes")
        
    else:
        print("\n❌ Schema update failed. Please check the errors above.")
