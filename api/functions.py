import os
import logging
from pinecone.grpc import PineconeGRPC as Pinecone
from openai import OpenAI

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Initialize Pinecone
try:
    pc = Pinecone(api_key=PINECONE_API_KEY)
    logger.info("Pinecone initialized successfully")
except Exception as e:
    logger.error(f"Error initializing Pinecone: {str(e)}")
    pc = None

# Define the index name and initialize the Pinecone index
index_name = "recipes"
try:
    index = pc.Index(index_name) if pc else None
    logger.info(f"Pinecone index '{index_name}' initialized successfully")
except Exception as e:
    logger.error(f"Error initializing Pinecone index: {str(e)}")
    index = None

try:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
    logger.info("OpenAI client initialized successfully")
except Exception as e:
    logger.error(f"Error initializing OpenAI client: {str(e)}")
    openai_client = None

def query_to_embedding(query):
    try:
        response = openai_client.embeddings.create(input=query, model="text-embedding-ada-002")
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Error creating embedding: {str(e)}")
        return None

def search_videos(query, top_k=30, namespace="All"):
    try:
        query_embedding = query_to_embedding(query)
        if query_embedding is None:
            return {"error": "Failed to create embedding"}

        if index is None:
            return {"error": "Pinecone index not initialized"}

        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
            namespace=namespace
        )
        return [
            {
                "object_id": match.id,
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
    except Exception as e:
        logger.error(f"Error in search_videos: {str(e)}")
        return {"error": str(e)}

def remove_video(video_id):
    try:
        if index is None:
            return {"error": "Pinecone index not initialized"}

        # Query the index to find the vector with the given video_id in metadata
        query_response = index.query(
            vector=[0] * 1536,  # Dummy vector, we're only interested in metadata
            filter={"video_id": {"$eq": video_id}},
            top_k=1,
            include_metadata=True
        )

        if not query_response.matches:
            return {"error": f"No video found with ID {video_id}"}

        # Get the Pinecone vector ID
        vector_id = query_response.matches[0].id

        # Delete the vector by its Pinecone ID
        index.delete(ids=[vector_id])
        logger.info(f"Video with ID {video_id} removed successfully")
        return {"success": True}
    except Exception as e:
        logger.error(f"Error in remove_video: {str(e)}")
        return {"error": str(e)}