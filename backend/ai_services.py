# ai_services.py - AI-powered service classification and matching

SERVICES = [
    {
        "id": "beauty_massage",
        "label": "Massage Therapy",
        "keywords": ["massage", "therapy", "relax", "spa", "wellness", "stress", "tension"],
        "followups": [
            {"id": "duration", "q": "How long would you like?", "type": "select", "options": ["30 min", "60 min", "90 min"]},
            {"id": "type", "q": "What type of massage?", "type": "select", "options": ["Swedish", "Deep Tissue", "Hot Stone", "Aromatherapy"]}
        ],
        "skill_tag": "beauty_wellness",
        "estimate_hours": [1, 1.5]
    },
    {
        "id": "home_cleaning",
        "label": "Home Cleaning",
        "keywords": ["clean", "cleaning", "house", "home", "dust", "vacuum", "mop", "tidy"],
        "followups": [
            {"id": "rooms", "q": "Which rooms need cleaning?", "type": "select", "options": ["All rooms", "Kitchen only", "Bathrooms only", "Bedrooms only"]},
            {"id": "frequency", "q": "How often?", "type": "select", "options": ["One-time", "Weekly", "Bi-weekly", "Monthly"]}
        ],
        "skill_tag": "cleaning",
        "estimate_hours": [1.5, 3]
    },
    {
        "id": "car_wash",
        "label": "Car Wash (Doorstep)",
        "keywords": ["car", "wash", "vehicle", "auto", "clean", "polish", "wax"],
        "followups": [
            {"id": "service_type", "q": "What type of wash?", "type": "select", "options": ["Basic wash", "Premium wash", "Full detail"]},
            {"id": "vehicle_size", "q": "Vehicle size?", "type": "select", "options": ["Sedan", "SUV", "Hatchback", "Truck"]}
        ],
        "skill_tag": "car_care",
        "estimate_hours": [0.75, 1.5]
    },
    {
        "id": "appliance_repair",
        "label": "Appliance Repair",
        "keywords": ["repair", "fix", "appliance", "broken", "not working", "refrigerator", "washing machine", "ac"],
        "followups": [
            {"id": "appliance", "q": "Which appliance?", "type": "select", "options": ["Refrigerator", "Washing Machine", "AC", "Microwave", "Other"]},
            {"id": "issue", "q": "What's the problem?", "type": "short"}
        ],
        "skill_tag": "appliance_repair",
        "estimate_hours": [1, 3]
    },
    {
        "id": "beauty_facial",
        "label": "Facial Treatment",
        "keywords": ["facial", "skin", "beauty", "glow", "acne", "treatment", "skincare"],
        "followups": [
            {"id": "skin_type", "q": "What's your skin type?", "type": "select", "options": ["Dry", "Oily", "Combination", "Sensitive"]},
            {"id": "concerns", "q": "Any specific concerns?", "type": "select", "options": ["Acne", "Aging", "Dark spots", "General glow"]}
        ],
        "skill_tag": "beauty_wellness",
        "estimate_hours": [1, 2]
    },
    {
        "id": "other",
        "label": "Something else",
        "keywords": [],
        "followups": [{"id": "describe", "q": "Tell us more about what you need", "type": "long"}],
        "skill_tag": "general",
        "estimate_hours": [0.5, 2]
    }
]

DEMO_LOC = {"lat": 40.7506, "lng": -73.9972}  # NYC area

PROVIDERS = [
    {
        "id": "p1",
        "name": "Luxury Spa Pro",
        "skill_tags": ["beauty_wellness"],
        "rate_hour": 1800,
        "avg_rating": 4.9,
        "lat": 40.754,
        "lng": -73.99,
        "service_radius_km": 20,
        "reliability": 0.9,
        "stats": {"beauty_wellness": {"jobs_done": 72, "completion_rate": 0.98}}
    },
    {
        "id": "p2",
        "name": "Clean Home Experts",
        "skill_tags": ["cleaning"],
        "rate_hour": 1500,
        "avg_rating": 4.7,
        "lat": 40.742,
        "lng": -73.99,
        "service_radius_km": 15,
        "reliability": 0.85,
        "stats": {"cleaning": {"jobs_done": 58, "completion_rate": 0.95}}
    },
    {
        "id": "p3",
        "name": "Auto Care Plus",
        "skill_tags": ["car_care"],
        "rate_hour": 800,
        "avg_rating": 4.6,
        "lat": 40.745,
        "lng": -74.004,
        "service_radius_km": 25,
        "reliability": 0.88,
        "stats": {"car_care": {"jobs_done": 120, "completion_rate": 0.97}}
    },
    {
        "id": "p4",
        "name": "Fix It Right",
        "skill_tags": ["appliance_repair"],
        "rate_hour": 2000,
        "avg_rating": 4.8,
        "lat": 40.761,
        "lng": -73.985,
        "service_radius_km": 30,
        "reliability": 0.92,
        "stats": {"appliance_repair": {"jobs_done": 210, "completion_rate": 0.99}}
    },
    {
        "id": "p5",
        "name": "Beauty Glow Studio",
        "skill_tags": ["beauty_wellness"],
        "rate_hour": 1600,
        "avg_rating": 4.9,
        "lat": 40.748,
        "lng": -73.99,
        "service_radius_km": 25,
        "reliability": 0.93,
        "stats": {"beauty_wellness": {"jobs_done": 340, "completion_rate": 0.98}}
    }
]
