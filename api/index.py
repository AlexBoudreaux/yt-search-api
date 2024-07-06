from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from functions import search_videos

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
async def search(query: str, top_k: int = 30, namespace: str = "All"):
    valid_namespaces = ["All", "Entree", "Side Dish", "Dessert", "Beverage", "Appetizer", "Snack", "Soup", "Salad", "Breakfast", "Condiment", "Dip", "Cocktail", "Other"]
    if namespace not in valid_namespaces:
        raise HTTPException(status_code=400, detail="Invalid namespace")
    try:
        results = search_videos(query, top_k, namespace)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def check():
    return {"message": "Healthy"}