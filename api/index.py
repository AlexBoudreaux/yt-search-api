from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello, World"}

@app.get("/api/hello")
async def hello():
    return {"message": "Hello from API"}

@app.get("/search")
async def search(query: str, top_k: int = 30, namespace: str = "All"):
    valid_namespaces = ["All", "Entree", "Side Dish", "Dessert", "Beverage", "Appetizer", "Snack", "Soup", "Salad", "Breakfast", "Condiment", "Dip", "Cocktail", "Other"]
    if namespace not in valid_namespaces:
        raise HTTPException(status_code=400, detail="Invalid namespace")
    
    # Placeholder response
    return {
        "query": query,
        "top_k": top_k,
        "namespace": namespace,
        "results": [
            {"title": "Sample Video 1", "description": "This is a sample video"},
            {"title": "Sample Video 2", "description": "This is another sample video"}
        ]
    }