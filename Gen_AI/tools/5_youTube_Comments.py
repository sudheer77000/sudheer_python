from googleapiclient.discovery import build

from dotenv import load_dotenv
import os
load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")
VIDEO_ID = "dQw4w9WgXcQ"

youtube = build("youtube", "v3", developerKey=API_KEY)

request = youtube.commentThreads().list(
    part="snippet",
    videoId=VIDEO_ID,
    maxResults=5,
    textFormat="plainText",
    order="relevance"
)

response = request.execute()

for item in response["items"]:
    comment = item["snippet"]["topLevelComment"]["snippet"]
    print(comment["authorDisplayName"])
    print(comment["textDisplay"])
    print("---")