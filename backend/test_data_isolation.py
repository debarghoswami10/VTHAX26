#!/usr/bin/env python3
"""
Test script to verify data isolation between users
"""

import requests
import json

def test_data_isolation():
    """Test that different users see different bookings"""
    
    # Test different customer IDs
    test_customers = [
        "bd00c24d-60f3-4146-a618-5f396d5ad491",
        "326b68aa-3a5c-45fb-bf31-2dfafb8a4bab", 
        "7c930000-dc10-4f13-b897-3df4bc2fd6c9"
    ]
    
    print("🧪 Testing Data Isolation Between Users")
    print("=" * 50)
    
    for customer_id in test_customers:
        try:
            response = requests.get(f"http://localhost:8000/bookings?customer_id={customer_id}")
            
            if response.status_code == 200:
                data = response.json()
                bookings = data.get('bookings', [])
                
                print(f"\n👤 Customer: {customer_id}")
                print(f"📊 Bookings count: {len(bookings)}")
                
                if bookings:
                    print("📋 Bookings:")
                    for booking in bookings:
                        print(f"  - ID: {booking.get('id')}, Status: {booking.get('status')}, Task: {booking.get('task', {}).get('title', 'N/A')}")
                else:
                    print("  No bookings found")
                    
            else:
                print(f"❌ Error for customer {customer_id}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exception for customer {customer_id}: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Data isolation test completed")

if __name__ == "__main__":
    test_data_isolation()
