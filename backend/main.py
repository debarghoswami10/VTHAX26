from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from supabase import create_client
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
from ai_integration import classify_service_request, get_service_followups, match_providers

load_dotenv()
app = FastAPI(title="Woke AI Platform", description="Premium in-house services with AI-powered matching")

# --------------------------
# CORS Middleware
# --------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------
# Supabase client
# --------------------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --------------------------
# Schemas
# --------------------------
class CustomerRegister(BaseModel):
    email: str
    password: str
    name: str

class TaskerRegister(BaseModel):
    email: str
    password: str
    name: str
    skills: list[str]
    hourly_rate: float
    bio: str

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    customer_id: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None  # open, in-progress, completed

class BookingCreate(BaseModel):
    task_id: int
    tasker_id: str
    customer_id: str

class BookingUpdate(BaseModel):
    status: str  # accepted, declined, completed

class ReviewCreate(BaseModel):
    booking_id: int
    rating: int
    review: Optional[str] = None

# --------------------------
# Root
# --------------------------
@app.get("/")
def root():
    return {"message": "Backend running"}

@app.get("/profiles")
def get_profiles():
    response = supabase.table("profiles").select("*").execute()
    return response.data

# --------------------------
# Registration Endpoints
# --------------------------
@app.post("/register/customer")
def register_customer(data: CustomerRegister):
    user = supabase.auth.sign_up({"email": data.email, "password": data.password})
    if not user.user:
        raise HTTPException(status_code=400, detail=user.get("message", "Signup failed"))

    supabase.table("profiles").insert({
        "id": user.user.id,
        "name": data.name,
        "role": "customer"
    }).execute()
    return {"message": "Customer registered", "user_id": user.user.id}

@app.post("/register/tasker")
def register_tasker(data: TaskerRegister):
    user = supabase.auth.sign_up({"email": data.email, "password": data.password})
    if not user.user:
        raise HTTPException(status_code=400, detail=user.get("message", "Signup failed"))

    supabase.table("profiles").insert({
        "id": user.user.id,
        "name": data.name,
        "role": "tasker",
        "skills": data.skills,
        "hourly_rate": data.hourly_rate,
        "bio": data.bio
    }).execute()
    return {"message": "Tasker registered", "tasker_id": user.user.id}

# --------------------------
# Tasks Endpoints
# --------------------------
@app.post("/tasks")
def create_task(data: TaskCreate):
    response = supabase.table("tasks").insert({
        "title": data.title,
        "description": data.description,
        "customer_id": data.customer_id
    }).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Failed to create task")
    return {"message": "Task created", "task": response.data}

@app.get("/tasks")
def list_tasks(customer_id: str):
    response = supabase.table("tasks").select("*").eq("customer_id", customer_id).execute()
    return {"tasks": response.data}

@app.patch("/tasks/{task_id}")
def update_task(task_id: int = Path(...), data: TaskUpdate = None):
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    response = supabase.table("tasks").update(update_data).eq("id", task_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Task not found or update failed")
    return {"message": "Task updated", "task": response.data}

# --------------------------
# Bookings Endpoints
# --------------------------
@app.post("/bookings")
def create_booking(data: BookingCreate):
    response = supabase.table("bookings").insert({
        "task_id": data.task_id,
        "customer_id": data.customer_id,
        "tasker_id": data.tasker_id,
        "status": "pending"
    }).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Failed to create booking")
    return {"message": "Booking created", "booking": response.data}

@app.get("/bookings")
def list_bookings(customer_id: str):
    response = supabase.table("bookings").select("*").eq("customer_id", customer_id).execute()
    return {"bookings": response.data}

@app.get("/bookings/tasker")
def list_tasker_bookings(tasker_id: str):
    response = supabase.table("bookings").select("*").eq("tasker_id", tasker_id).execute()
    return {"bookings": response.data}

@app.patch("/bookings/{booking_id}")
def update_booking(booking_id: int, data: BookingUpdate):
    response = supabase.table("bookings").update({"status": data.status}).eq("id", booking_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Booking not found or update failed")
    return {"message": f"Booking updated to {data.status}", "booking": response.data}

# --------------------------
# Reviews Endpoints
# --------------------------
@app.post("/reviews")
def create_review(data: ReviewCreate):
    if data.rating < 1 or data.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be 1-5")
    response = supabase.table("reviews").insert({
        "booking_id": data.booking_id,
        "rating": data.rating,
        "review": data.review
    }).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Failed to create review")
    return {"message": "Review submitted", "review": response.data}

@app.get("/reviews/{tasker_id}")
def list_tasker_reviews(tasker_id: str):
    response = supabase.table("reviews").select("*").eq("tasker_id", tasker_id).execute()
    return {"reviews": response.data}

# --------------------------
# AI Integration Endpoints
# --------------------------
class ClassifyRequest(BaseModel):
    text: str

class FollowupRequest(BaseModel):
    service_id: str
    answers: Dict[str, Any] = {}

class MatchRequest(BaseModel):
    service_id: str
    spec: Dict[str, Any] = {}
    location: Optional[Dict[str, float]] = None

@app.post("/api/ai/classify")
async def classify_service(data: ClassifyRequest):
    try:
        result = await classify_service_request(data.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")

@app.post("/api/ai/followups")
def get_service_followups_endpoint(data: FollowupRequest):
    try:
        result = get_service_followups(data.service_id, data.answers)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Followup generation failed: {str(e)}")

@app.post("/api/ai/match")
def match_service_providers(data: MatchRequest):
    try:
        result = match_providers(data.service_id, data.spec, data.location)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Provider matching failed: {str(e)}")

@app.get("/api/ai/health")
def ai_health_check():
    return {"status": "healthy", "ai_enabled": True, "ollama_url": "http://localhost:11434"}
