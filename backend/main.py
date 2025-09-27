from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from supabase import create_client
from pydantic import BaseModel
from jose import jwt
from typing import Optional, Dict, Any
import os
from ai_integration import classify_service_request, get_service_followups, match_providers

load_dotenv()
app = FastAPI(title="Woke AI Platform", description="Premium in-house services with AI-powered matching")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()  # For Authorization header

# Supabase client
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")  # You can get this from Supabase -> Settings -> API

# --------------------------
# Auth helper
# --------------------------
def get_current_user(authorization: str = Header(...)):
    token = authorization.split(" ")[1]  # "Bearer <token>"
    try:
        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"])
        return payload["sub"]  # This is the user id
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

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
    customer_id: str  # included in body

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class BookingCreate(BaseModel):
    task_id: int
    tasker_id: str  # UUID of the tasker
    customer_id: str  # included in body
    # status defaults to 'pending'

class BookingUpdate(BaseModel):
    status: Optional[str] = None

# --------------------------
# Supabase client
# --------------------------
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

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
    # Create auth user
    user = supabase.auth.sign_up({
        "email": data.email,
        "password": data.password
    })

    if not user.user:
        raise HTTPException(status_code=400, detail=user.get("message", "Signup failed"))

    # Insert into profiles
    supabase.table("profiles").insert({
        "id": user.user.id,
        "name": data.name,
        "role": "customer"
    }).execute()

    return {"message": "Customer registered", "user_id": user.user.id}

@app.post("/register/tasker")
def register_tasker(data: TaskerRegister):
    # Create auth user
    user = supabase.auth.sign_up({
        "email": data.email,
        "password": data.password
    })

    if not user.user:
        raise HTTPException(status_code=400, detail=user.get("message", "Signup failed"))

    # Insert into profiles
    supabase.table("profiles").insert({
        "id": user.user.id,
        "name": data.name,
        "role": "tasker",
        "skills": data.skills,
        "hourly_rate": data.hourly_rate,
        "bio": data.bio
    }).execute()

    return {"message": "Tasker registered", "tasker_id": user.user.id}

# AI Integration Schemas
class ClassifyRequest(BaseModel):
    text: str

class FollowupRequest(BaseModel):
    service_id: str
    answers: Dict[str, Any] = {}

class MatchRequest(BaseModel):
    service_id: str
    spec: Dict[str, Any] = {}
    location: Optional[Dict[str, float]] = None

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
def update_booking(booking_id: int, data: BookingUpdate, current_user: str = Depends(get_current_user)):
    response = supabase.table("bookings").update({
        "status": data.status
    }).eq("id", booking_id).eq("tasker_id", current_user).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"message": "Booking updated", "booking": response.data}

# --------------------------
# AI Integration Endpoints
# --------------------------
@app.post("/api/ai/classify")
async def classify_service(data: ClassifyRequest):
    """
    Classify user's service request into specific service categories using AI.
    """
    try:
        result = await classify_service_request(data.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")

@app.post("/api/ai/followups")
def get_service_followups_endpoint(data: FollowupRequest):
    """
    Get follow-up questions for a specific service.
    """
    try:
        result = get_service_followups(data.service_id, data.answers)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Followup generation failed: {str(e)}")

@app.post("/api/ai/match")
def match_service_providers(data: MatchRequest):
    """
    Match service providers based on service requirements and location.
    """
    try:
        result = match_providers(data.service_id, data.spec, data.location)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Provider matching failed: {str(e)}")

@app.get("/api/ai/health")
def ai_health_check():
    """
    Health check for AI services.
    """
    return {"status": "healthy", "ai_enabled": True, "ollama_url": "http://localhost:11434"}
