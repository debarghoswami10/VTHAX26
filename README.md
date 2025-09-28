# Woke Platform

**Premium in-house services with AI-powered matching.**  
This repository contains the Woke platform frontend and backend. Users can browse service providers, book tasks, and manage bookings. The backend uses FastAPI and Supabase for database and authentication, while the frontend is built with HTML, TailwindCSS, and JavaScript.

---

## Features

- Customer and provider registration/login.
- Browse service providers by category (Cleaning, Repairs, Beauty, etc.).
- Book services with task details linked to customer accounts.
- Review and rating system for taskers.
- Mock checkout/payment flow.

---

## Getting Started (Local Development Only)

### 1. Clone the Repository
 - Install GitHub Desktop
 - Go to File -> Clone Repository (or click Ctrl + Shift + O)
 - Click the URL section and copy and paste this link: "https://github.com/shri4anand/VTHAX25-2.git"


### 2. Setup Backend
- Type into terminal
   ```
   cd backend copy
   ```
- or right-click the folder "backend copy" and click "Open in Terminal"
   
- Create Virtual Environment : python -m venv venv
- Activate it:
 ```
python -m venv venv
.\venv\Scripts\activate               #  Windows
source venv/bin/activate            #  macOS/Linux
```
- Install dependencies:
  ```
  pip install -r requirements.txt
  ```
- If the step above doesn't work, copy and paste this statement into the venv:
  ```
      pip install fastapi uvicorn python-dotenv supabase pydantic "python-jose[cryptography]"
      python.exe -m pip install --upgrade pip
      pip install ipython black
      pip install python-jose python-dotenv
  
  ```

- Run your backend:
 ```
uvicorn main:app --reload
```
### 3. Opening index.file
- Direct to frontend copy -> index file
- Right-click the file and open in a new tab/window
