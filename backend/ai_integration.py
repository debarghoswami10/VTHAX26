# ai_integration.py - AI-powered service classification and matching integration

import httpx
import math
from typing import List, Dict, Any, Optional
from ai_services import SERVICES, PROVIDERS, DEMO_LOC

OLLAMA_URL = 'http://localhost:11434'

def haversine_km(a: Dict[str, float], b: Dict[str, float]) -> float:
    """Calculate distance between two points in kilometers using Haversine formula."""
    to_rad = lambda d: d * math.pi / 180
    R = 6371
    d_lat = to_rad(b["lat"] - a["lat"])
    d_lng = to_rad(b["lng"] - a["lng"])
    lat1 = to_rad(a["lat"])
    lat2 = to_rad(b["lat"])
    x = math.sin(d_lat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lng/2)**2
    return 2 * R * math.asin(math.sqrt(x))

def normalize(x: float, lo: float, hi: float) -> float:
    """Normalize value between 0 and 1."""
    if hi <= lo:
        return 0
    v = (x - lo) / (hi - lo)
    return max(0, min(1, v))

async def classify_service_request(text: str) -> Dict[str, Any]:
    """
    Classify vague service requests into specific service categories using AI.
    
    Args:
        text: User's service request text
        
    Returns:
        Dictionary with classified service candidates
    """
    if not text:
        return {"candidates": []}
    
    # Prepare system prompt for AI classification
    service_ids = [s["id"] for s in SERVICES]
    sys_prompt = f"""You classify vague home-service requests into up to 6 candidate intents with reasons.
Return STRICT JSON: {{"candidates":[{{"service_id":"...","reason":"...","confidence":0-1}}]}}
Use ONLY these IDs: {', '.join(service_ids)}."""
    
    prompt = f"{sys_prompt}\n\nUSER: \"{text}\""
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": "llama3.1:8b",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30.0
            )
            data = response.json()
            
            # Try to parse AI response
            try:
                parsed = {"candidates": []}
                if "response" in data:
                    import json
                    parsed = json.loads(data["response"])
            except:
                pass
            
            # Fallback if AI returns non-JSON or empty response
            if not parsed.get("candidates"):
                lower_text = text.lower()
                hits = [s for s in SERVICES if any(k in lower_text for k in s["keywords"])]
                if not hits:
                    hits = SERVICES[:3]  # Default to first 3 services
                
                parsed["candidates"] = [
                    {
                        "service_id": s["id"],
                        "reason": f"Candidate: {s['label']}",
                        "confidence": 0.5
                    }
                    for s in hits
                ]
            
            # Enrich with labels and limit to 5 candidates
            enriched_candidates = []
            for candidate in parsed["candidates"][:5]:
                service = next((s for s in SERVICES if s["id"] == candidate["service_id"]), None)
                if service:
                    enriched_candidates.append({
                        **candidate,
                        "label": service["label"]
                    })
            
            return {"candidates": enriched_candidates}
            
    except Exception as e:
        # Fallback to keyword matching
        lower_text = text.lower()
        hits = [s for s in SERVICES if any(k in lower_text for k in s["keywords"])]
        if not hits:
            hits = SERVICES[:3]
        
        return {
            "candidates": [
                {
                    "service_id": s["id"],
                    "label": s["label"],
                    "reason": f"Keyword match: {s['label']}",
                    "confidence": 0.5
                }
                for s in hits[:5]
            ]
        }

def get_service_followups(service_id: str, answers: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Get follow-up questions for a specific service.
    
    Args:
        service_id: ID of the selected service
        answers: Previously provided answers
        
    Returns:
        Dictionary with next questions and readiness status
    """
    if answers is None:
        answers = {}
    
    service = next((s for s in SERVICES if s["id"] == service_id), None)
    if not service:
        return {"error": "unknown_service"}
    
    # Filter out already answered questions
    next_questions = []
    for followup in service.get("followups", []):
        if followup["id"] not in answers:
            next_questions.append(followup)
    
    return {
        "next": next_questions,
        "ready": len(next_questions) == 0,
        "estimate_hours": service.get("estimate_hours", [1, 2])
    }

def match_providers(service_id: str, spec: Dict[str, Any] = None, location: Dict[str, float] = None) -> Dict[str, Any]:
    """
    Match service providers based on service requirements and location.
    
    Args:
        service_id: ID of the selected service
        spec: Service specifications from followup answers
        location: User's location coordinates
        
    Returns:
        Dictionary with matched providers
    """
    if spec is None:
        spec = {}
    if location is None:
        location = DEMO_LOC
    
    service = next((s for s in SERVICES if s["id"] == service_id), None)
    if not service:
        return {"error": "unknown_service"}
    
    # Filter providers by skill
    capable_providers = []
    for provider in PROVIDERS:
        if service["skill_tag"] in provider.get("skill_tags", []):
            distance = haversine_km(location, {"lat": provider["lat"], "lng": provider["lng"]})
            if distance <= provider.get("service_radius_km", 20):
                capable_providers.append({**provider, "distance_km": distance})
    
    if not capable_providers:
        return {"providers": []}
    
    # Score and sort providers
    rate_values = [p["rate_hour"] for p in capable_providers]
    min_rate = min(rate_values)
    max_rate = max(rate_values)
    
    scored_providers = []
    for provider in capable_providers:
        stats = provider.get("stats", {}).get(service["skill_tag"], {"jobs_done": 0, "completion_rate": 0.9})
        
        # Calculate scoring factors
        factors = {
            "skill": 1.0,  # Has the required skill
            "success": stats.get("completion_rate", 0.9),
            "distance": normalize(
                provider.get("service_radius_km", 20) - provider["distance_km"],
                0, provider.get("service_radius_km", 20)
            ),
            "rating": (provider.get("avg_rating", 4.5)) / 5,
            "price": 1 - normalize(provider["rate_hour"], min_rate, max_rate),
            "availability": 0.8,  # Assume good availability
            "reliability": provider.get("reliability", 0.85),
            "experience": min(stats.get("jobs_done", 0) / 100, 1.0)  # Normalize experience
        }
        
        # Weighted scoring
        weights = {
            "skill": 0.25,
            "success": 0.2,
            "distance": 0.15,
            "rating": 0.15,
            "price": 0.1,
            "availability": 0.1,
            "reliability": 0.05
        }
        
        score = sum(factors[key] * weights[key] for key in weights)
        scored_providers.append({"provider": provider, "factors": factors, "score": score})
    
    # Sort by score and take top 3
    scored_providers.sort(key=lambda x: x["score"], reverse=True)
    top_providers = scored_providers[:3]
    
    # Format response
    providers = []
    for item in top_providers:
        provider = item["provider"]
        stats = provider.get("stats", {}).get(service["skill_tag"], {"jobs_done": 0, "completion_rate": 0.9})
        
        eta_min = 20 if item["factors"]["distance"] > 0.5 else 12
        reason_line = f"{provider['name']} — {stats['jobs_done']} similar jobs ({int(stats['completion_rate'] * 100)}%), ~{eta_min} min away, ₹{provider['rate_hour']}/hr."
        
        providers.append({
            "id": provider["id"],
            "name": provider["name"],
            "rate_hour": provider["rate_hour"],
            "avg_rating": provider["avg_rating"],
            "eta_min": eta_min,
            "reason_line": reason_line
        })
    
    return {"providers": providers}
