from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.security import HTTPBearer
from dotenv import load_dotenv
from supabase import create_client
from pydantic import BaseModel
from jose import jwt
import os

load_dotenv()
app = FastAPI()
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
class TaskCreate(BaseModel):
    title: str
    description: str | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None

class BookingCreate(BaseModel):
    task_id: int
    tasker_id: str

class BookingUpdate(BaseModel):
    status: str

# --------------------------
# Tasks Endpoints
# --------------------------
@app.post("/tasks")
def create_task(data: TaskCreate, current_user: str = Depends(get_current_user)):
    response = supabase.table("tasks").insert({
        "customer_id": current_user,
        "title": data.title,
        "description": data.description
    }).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"message": "Task created", "task": response.data}

@app.get("/tasks")
def get_customer_tasks(current_user: str = Depends(get_current_user)):
    response = supabase.table("tasks").select("*").eq("customer_id", current_user).execute()
    return response.data

@app.get("/tasks/available")
def get_available_tasks():
    response = supabase.table("tasks").select("*").eq("status", "open").execute()
    return response.data

@app.patch("/tasks/{task_id}")
def update_task(task_id: int, data: TaskUpdate, current_user: str = Depends(get_current_user)):
    updates = {k: v for k, v in data.dict().items() if v is not None}
    response = supabase.table("tasks").update(updates).eq("id", task_id).eq("customer_id", current_user).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"message": "Task updated", "task": response.data}

# --------------------------
# Bookings Endpoints
# --------------------------
@app.post("/bookings")
def create_booking(data: BookingCreate, current_user: str = Depends(get_current_user)):
    response = supabase.table("bookings").insert({
        "task_id": data.task_id,
        "customer_id": current_user,
        "tasker_id": data.tasker_id
    }).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"message": "Booking created", "booking": response.data}

@app.get("/bookings")
def get_tasker_bookings(current_user: str = Depends(get_current_user)):
    response = supabase.table("bookings").select("*").eq("tasker_id", current_user).execute()
    return response.data

@app.patch("/bookings/{booking_id}")
def update_booking(booking_id: int, data: BookingUpdate, current_user: str = Depends(get_current_user)):
    response = supabase.table("bookings").update({
        "status": data.status
    }).eq("id", booking_id).eq("tasker_id", current_user).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"message": "Booking updated", "booking": response.data}
