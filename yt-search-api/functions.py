from ast import literal_eval
import pandas as pd
import numpy as np
import openai
import os
from supabase import create_client
# from openai import OpenAI


# Set API keys from environment variables
openai.api_key = os.environ.get("OPENAI_API_KEY")
# client = OpenAI(api_key="")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Connect to Supabase
def create_supabase_client(url, key):
    return create_client(url, key)

# Retrieve Video Data from Supabase
def get_videos_from_supabase(client):
    # Query to select only cooking videos
    query = client.table('videos').select('*').eq('category', 'Cooking')
    
    # Execute the query and fetch the data
    data = query.execute()
    
    # Convert the data to a DataFrame
    return pd.DataFrame(data.data)

# Convert query to embedding using OpenAI's Ada model
def query_to_embedding(query):
    response = openai.Embedding.create(input=query, model="text-embedding-ada-002")
    # print(response)
    embedding = response.data[0].embedding
    return embedding

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search_videos(query, videos_df, threshold=0.8):
    # Get embeddings for the query
    query_embedding = query_to_embedding(query)

    # Check and convert embeddings if necessary
    if isinstance(videos_df['embedding'].iloc[0], str):
        videos_df['embedding'] = videos_df['embedding'].apply(literal_eval)

    # Filter out rows where embedding is None
    videos_df = videos_df[videos_df['embedding'].notnull()]

    # Calculate similarities
    videos_df['similarity'] = videos_df['embedding'].apply(lambda x: cosine_similarity(query_embedding, x))

    # Filter videos based on the similarity threshold
    filtered_videos = videos_df[videos_df['similarity'] >= threshold]

    # Sorting by similarity
    sorted_videos = filtered_videos.sort_values(by='similarity', ascending=False)

    # Return the necessary columns
    return sorted_videos[['video_name', 'creator', 'video_id']]  # Add any other needed columns here




# Main function to run the search
def main():
    client = create_supabase_client(SUPABASE_URL, SUPABASE_KEY)
    query = input("Enter your search query: ")
    top_videos = search_videos(query, client)
    print("Top videos for your query:")
    print(top_videos)

if __name__ == "__main__":
    main()
