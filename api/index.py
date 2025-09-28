# This file is needed for Vercel to recognize the API routes
# It imports the main FastAPI app from the backend directory
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from main import app

# Export the app for Vercel
handler = app
