from fastapi import FastAPI
from dotenv import load_dotenv
from supabase import create_client
from pydantic import BaseModel
from fastapi.exceptions import HTTPException
import os

load_dotenv()
app = FastAPI()

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
    description: str | None = None
    customer_id: str  # included in body

class BookingCreate(BaseModel):
    task_id: int
    tasker_id: str  # UUID of the tasker
    customer_id: str  # included in body
    # status defaults to 'pending'

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