from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()  # Load variables from .env

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")  # Fetch API key


# Mood-to-Genre Mapping
MOOD_GENRE_MAP = {
    "happy": "Pop",
    "sad": "Blues",
    "energetic": "Rock",
    "relaxed": "Jazz",
    "romantic": "R&B",
    "angry": "Metal",
    "calm": "Classical",
    "excited": "EDM",
}

# Function to analyze mood using TextBlob
def analyze_mood(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    if polarity > 0.5:
        return "happy"
    elif polarity > 0.2:
        return "excited"
    elif polarity > 0:
        return "relaxed"
    elif polarity == 0:
        return "calm"
    elif polarity < -0.5:
        return "sad"
    elif polarity < -0.2:
        return "angry"
    else:
        return "neutral"

# Function to fetch a YouTube song based on genre
# Initialize YouTube API client
def fetch_song(genre):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)  # Add this line
    search_query = f"best {genre} songs"
    
    request = youtube.search().list(
        q=search_query,
        part="snippet",
        type="video",
        maxResults=1
    )
    response = request.execute()
    
    if "items" in response and response["items"]:
        video = response["items"][0]
        return {
            "video_id": video["id"]["videoId"],
            "video_title": video["snippet"]["title"]
        }
    return {"video_id": None, "video_title": "No video found"}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    text = request.form.get("text")
    
    if not text:
        return jsonify({"error": "No input provided"}), 400
    
    mood = analyze_mood(text)
    genre = MOOD_GENRE_MAP.get(mood, "Pop")  # Default to Pop if mood not mapped
    song = fetch_song(genre)
    
    return jsonify({
        "mood": mood.capitalize(),
        "genre": genre,
        "video_title": song["video_title"],
        "video_id": song["video_id"]
    })

if __name__ == "__main__":
    app.run(debug=True)
