#!/usr/bin/env python3
"""
Test script for AI integration without running the full server
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_integration import classify_service_request, get_service_followups, match_providers

async def test_ai_integration():
    print("🧪 Testing AI Integration for VTHAX26 'woke' Platform")
    print("=" * 60)
    
    # Test 1: Service Classification
    print("\n1️⃣ Testing Service Classification")
    print("-" * 40)
    
    test_queries = [
        "I need a massage",
        "My house needs cleaning",
        "Car wash service",
        "Fix my broken washing machine",
        "I want a facial treatment"
    ]
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        try:
            result = await classify_service_request(query)
            candidates = result.get("candidates", [])
            for i, candidate in enumerate(candidates[:3], 1):
                print(f"  {i}. {candidate['label']} (confidence: {candidate.get('confidence', 0):.2f})")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    # Test 2: Followup Questions
    print("\n\n2️⃣ Testing Followup Questions")
    print("-" * 40)
    
    test_services = ["massage_therapy", "home_cleaning", "car_wash"]
    
    for service_id in test_services:
        print(f"\nService: {service_id}")
        try:
            result = get_service_followups(service_id, {})
            next_questions = result.get("next", [])
            print(f"  Questions to ask: {len(next_questions)}")
            for q in next_questions:
                print(f"    - {q['q']} ({q['type']})")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    # Test 3: Provider Matching
    print("\n\n3️⃣ Testing Provider Matching")
    print("-" * 40)
    
    test_matches = [
        ("massage_therapy", {"duration": "60 min", "type": "Swedish"}),
        ("home_cleaning", {"rooms": "All rooms", "frequency": "One-time"}),
        ("car_wash", {"service_type": "Premium wash", "vehicle_size": "SUV"})
    ]
    
    for service_id, spec in test_matches:
        print(f"\nService: {service_id}")
        print(f"Spec: {spec}")
        try:
            result = match_providers(service_id, spec)
            providers = result.get("providers", [])
            print(f"  Found {len(providers)} providers:")
            for i, provider in enumerate(providers, 1):
                print(f"    {i}. {provider['name']} - ₹{provider['rate_hour']}/hr")
                print(f"       Rating: {provider['avg_rating']}, ETA: {provider['eta_min']} min")
                print(f"       {provider['reason_line']}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("\n\n✅ AI Integration Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_ai_integration())
