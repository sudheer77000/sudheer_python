from youtube_transcript_api import YouTubeTranscriptApi
import time

video_id = "PtG9_Zbm7Jw"

api = YouTubeTranscriptApi()
transcript = api.fetch(video_id)

text = "\n".join(snippet.text for snippet in transcript)

# Print like typing
for char in text:
    print(char, end="", flush=True)
    time.sleep(0.02)  # typing speed

print()