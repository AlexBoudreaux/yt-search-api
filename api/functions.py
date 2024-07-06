import os
from pinecone.grpc import PineconeGRPC as Pinecone
from openai import OpenAI

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Define the index name and initialize the Pinecone index
index_name = "recipes"
index = pc.Index(index_name)

openai_client = OpenAI(api_key=OPENAI_API_KEY)

def query_to_embedding(query):
    response = openai_client.embeddings.create(input=query, model="text-embedding-ada-002")
    return response.data[0].embedding

def search_videos(query, top_k=30, namespace="All"):
    query_embedding = query_to_embedding(query)
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        namespace=namespace
    )
    return [
        {
            "video_name": match.metadata.get("title"),
            "creator": match.metadata.get("creator"),
            "video_id": match.metadata.get("video_id"),
            "url": match.metadata.get("url"),
            "description": match.metadata.get("description"),
            "food_category": match.metadata.get("food_category"),
            "personalized_description": match.metadata.get("personalized_description"),
            "recipe": match.metadata.get("recipe"),
            "transcript": match.metadata.get("transcript"),
            "score": match.score
        }
        for match in results.matches
    ]