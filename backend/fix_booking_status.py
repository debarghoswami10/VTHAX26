#!/usr/bin/env python3
"""
Fix booking status constraint to support Uber-like statuses
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

def fix_booking_status_constraint():
    """Update booking status constraint to support Uber-like statuses"""
    
    print("🔧 Fixing booking status constraint for Uber-like functionality...")
    
    try:
        # Drop existing constraint
        print("1. Dropping existing status constraint...")
        supabase.rpc('exec_sql', {
            'sql': "ALTER TABLE bookings DROP CONSTRAINT IF EXISTS bookings_status_check;"
        }).execute()
        print("   ✅ Existing constraint dropped")
        
        # Add new constraint with Uber-like statuses
        print("2. Adding new status constraint...")
        supabase.rpc('exec_sql', {
            'sql': "ALTER TABLE bookings ADD CONSTRAINT bookings_status_check CHECK (status IN ('pending','accepted','in-progress','completed','cancelled','declined'));"
        }).execute()
        print("   ✅ New constraint added")
        
        print("\n✅ Booking status constraint updated successfully!")
        print("📋 Supported statuses:")
        print("   • pending - Waiting for provider to accept")
        print("   • accepted - Provider has accepted the booking")
        print("   • in-progress - Service is currently being performed")
        print("   • completed - Service has been completed")
        print("   • cancelled - Booking was cancelled by customer")
        print("   • declined - Booking was declined by provider")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating constraint: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Fixing booking status constraint...")
    print("=" * 50)
    
    if fix_booking_status_constraint():
        print("\n🎉 Booking system now supports Uber-like statuses!")
    else:
        print("\n❌ Failed to update booking status constraint.")
