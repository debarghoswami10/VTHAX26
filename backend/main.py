from fastapi import FastAPI
from dotenv import load_dotenv
from supabase import create_client
from pydantic import BaseModel
from fastapi.exceptions import HTTPException
import os

load_dotenv()
app = FastAPI()

# --------------------------
# Asking for schemas
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

# --------------------------
# Supabase client
# --------------------------
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

@app.get("/")
def root():
    return {"message": "Backend running"}

@app.get("/profiles")
def get_profiles():
    response = supabase.table("profiles").select("*").execute()
    return response.data

# --------------------------
# Endpoints
# --------------------------
@app.post("/register/customer")
def register_customer(data: CustomerRegister):
    # 1. Create auth user
    user = supabase.auth.sign_up({
        "email": data.email,
        "password": data.password
    })

    if not user.user:
        raise HTTPException(status_code=400, detail=user.get("message", "Signup failed"))

    # 2. Insert into profiles
    supabase.table("profiles").insert({
        "id": user.user.id,
        "name": data.name,
        "role": "customer"
    }).execute()

    return {"message": "Customer registered", "user_id": user.user.id}

@app.post("/register/tasker")
def register_tasker(data: TaskerRegister):
    # 1. Create auth user
    user = supabase.auth.sign_up({
        "email": data.email,
        "password": data.password
    })

    if not user.user:
        raise HTTPException(status_code=400, detail=user.get("message", "Signup failed"))

    # 2. Insert into profiles
    supabase.table("profiles").insert({
        "id": user.user.id,
        "name": data.name,
        "role": "tasker",
        "skills": data.skills,
        "hourly_rate": data.hourly_rate,
        "bio": data.bio
    }).execute()

    return {"message": "Tasker registered", "user_id": user.user.id}