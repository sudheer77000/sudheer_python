from youtube_transcript_api import YouTubeTranscriptApi

video_id = "zW2GaUwDQyA"

api = YouTubeTranscriptApi()
transcript = api.fetch(video_id)

text = "\n".join(snippet.text for snippet in transcript)

print(text)