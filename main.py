from ast import literal_eval
import pandas as pd
import numpy as np
import json
import openai
# from openai import OpenAI

# client = OpenAI(api_key="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")
openai.api_key = "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"

from supabase import create_client

# Supabase credentials
SUPABASE_URL = 'https://bbrcyfqrvwqbboudayre.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJicmN5ZnFydndxYmJvdWRheXJlIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTQ1Nzc0MzAsImV4cCI6MjAxMDE1MzQzMH0.SPNLpnm_cIHUdYMOKOK4d56VmgfNpuTComWRigMBwTg'

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

def search_videos(query, client, top_k=6):
    # Get embeddings for the query
    query_embedding = query_to_embedding(query)

    # Fetch all video data
    videos_df = get_videos_from_supabase(client)

    # Check and convert embeddings if necessary
    if isinstance(videos_df['embedding'].iloc[0], str):
        videos_df['embedding'] = videos_df['embedding'].apply(literal_eval)

    # Filter out rows where embedding is None
    videos_df = videos_df[videos_df['embedding'].notnull()]

    # Calculate similarities
    videos_df['similarity'] = videos_df['embedding'].apply(lambda x: cosine_similarity(query_embedding, x))

    # Sorting and selection
    top_videos = videos_df.sort_values(by='similarity', ascending=False).head(top_k)

    # Return the necessary columns
    return top_videos[['video_name', 'creator', 'video_id']]  # Add any other needed columns here



# Main function to run the search
def main():
    client = create_supabase_client(SUPABASE_URL, SUPABASE_KEY)
    query = input("Enter your search query: ")
    top_videos = search_videos(query, client)
    print("Top videos for your query:")
    print(top_videos)

if __name__ == "__main__":
    main()
