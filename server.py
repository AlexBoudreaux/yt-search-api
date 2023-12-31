from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import pandas as pd
from main import create_supabase_client, search_videos, get_videos_from_supabase, SUPABASE_URL, SUPABASE_KEY

# Initialize FastAPI app
app = FastAPI()

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust as necessary for production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Initialize your Supabase client outside of the endpoint
client = create_supabase_client(SUPABASE_URL, SUPABASE_KEY)

# Fetch all video data
videos_df = get_videos_from_supabase(client)

@app.get("/search/")
async def search(query: str, threshold: float = 0.77):
    try:
        top_videos = search_videos(query, videos_df, threshold)
        return top_videos.to_dict(orient='records')  # Convert DataFrame to a list of dicts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))