import logging
import os
import uvicorn
from app.api.routers.chat import chat_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import datetime
from pydantic import BaseModel

from supabase import create_client, Client

app = FastAPI()

environment = os.getenv("ENVIRONMENT", "dev")  # Default to 'development' if not set

class Feedback(BaseModel):
    user_query: str
    created_at: str = datetime.datetime.now()

if environment == "dev":
    logger = logging.getLogger("uvicorn")
    logger.warning("Running in development mode - allowing CORS for all origins")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/health", status_code=200)
async def health():
    return {"status": "success"}


app.include_router(chat_router, prefix="/api/chat")

SUPABASE_DB_URL = os.environ["SUPABASE_DB_URL"]
SUPABASE_DB_KEY = os.environ["SUPABASE_DB_KEY"]

url = SUPABASE_DB_URL
key = SUPABASE_DB_KEY

supabase = create_client(url, key)

@app.post("/supabase/add")
async def add(feedback: Feedback):
    # supabase.table('response').insert({"created_at": str(datetime.now()), "user_query": "Is it working?"}).execute()
    supabase.table('response').insert({"created_at": feedback.created_at, "user_query": feedback.user_query}).execute()
    return {"status": "success"}



if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=80, reload=False)
