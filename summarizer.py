from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
import re

def get_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/)([^\s&]+)", url)
    return match.group(1) if match else None

def get_transcription(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return " ".join([entry['text'] for entry in transcript])

def split_text(text, max_words=500):
    words = text.split()
    return [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]

def summarize_text(text):
    model_name = "facebook/bart-large-cnn"
    summarizer = pipeline("summarization", model=model_name)

    chunks = split_text(text, max_words=500)

    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=150, min_length=40, do_sample=False)[0]["summary_text"]
        summaries.append(summary)

    return " ".join(summaries)

def summarize_video(url):
    video_id = get_video_id(url)
    if not video_id:
        return "URL inválida."
    transcript = get_transcription(video_id)
    return summarize_text(transcript)
