from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .functions import search_videos, remove_video
import logging

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"Health": "OK"}

@app.get("/search")
async def search(query: str, top_k: int = 30, namespace: str = "All"):
    valid_namespaces = ["All", "Entree", "Side Dish", "Dessert", "Beverage", "Appetizer", "Snack", "Soup", "Salad", "Breakfast", "Condiment", "Dip", "Cocktail", "Other"]
    if namespace not in valid_namespaces:
        raise HTTPException(status_code=400, detail="Invalid namespace")
    try:
        results = search_videos(query, top_k, namespace)
        if isinstance(results, dict) and "error" in results:
            logger.error(f"Error in search: {results['error']}")
            raise HTTPException(status_code=500, detail=results['error'])
        return results
    except Exception as e:
        logger.error(f"Unexpected error in search: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/remove_video/{video_id}")
async def remove_video_endpoint(video_id: str):
    try:
        result = remove_video(video_id)
        if isinstance(result, dict) and "error" in result:
            logger.error(f"Error in remove_video: {result['error']}")
            raise HTTPException(status_code=500, detail=result['error'])
        return {"message": f"Video with ID {video_id} removed successfully"}
    except Exception as e:
        logger.error(f"Unexpected error in remove_video: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))