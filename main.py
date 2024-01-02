from flask import Flask, request, jsonify
from flask_cors import CORS
from http import HTTPStatus
import os
from functions import create_supabase_client, search_videos, get_videos_from_supabase, SUPABASE_URL, SUPABASE_KEY

app = Flask(__name__)

CORS(app)

client = create_supabase_client(SUPABASE_URL, SUPABASE_KEY)

# Fetch all video data
videos_df = get_videos_from_supabase(client)

@app.route("/search")
def search():
    """Return top videos based on query and threshold"""
    query = request.args.get('query', default='', type=str)
    threshold = request.args.get('threshold', default=0.77, type=float)
    try:
        top_videos = search_videos(query, videos_df, threshold)
        return jsonify(top_videos.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@app.route("/")
def check():
    """Health Check"""
    return {"message": "Healthy"}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))