import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
load_dotenv()

# Ensure ADC is set from the environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Configure Google Generative AI API (authentication handled by Application Default Credentials)
genai.configure()

# Prompt template
prompt = """
You are a YouTube video summarizer. You will take the transcript text and summarize the entire video, 
providing the important summary in bullet points within 250 words. Please provide the summary of the text given here: 
"""

# Function to extract transcript from YouTube video
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for item in transcript_data:
            transcript += " " + item["text"]

        return transcript

    except Exception as e:
        st.error(f"Error extracting transcript: {str(e)}")
        return None

# Function to generate summary using Google Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    try:
        # Use keyword arguments, not positional ones
        response = genai.generate_text(model="text-bison-001", prompt=prompt + transcript_text)
        return response['candidates'][0]['output']  # Accessing the correct part of the response

    except Exception as e:
        st.error(f"Error generating summary: {str(e)}")
        return None

# Streamlit app interface
st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    try:
        video_id = youtube_link.split("=")[1]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    except IndexError:
        st.error("Invalid YouTube URL format. Please enter a valid URL.")

# Button to get detailed notes
if st.button("Get Detailed Notes"):
    if youtube_link:
        transcript_text = extract_transcript_details(youtube_link)

        if transcript_text:
            st.info("Transcript extracted successfully!")
            summary = generate_gemini_content(transcript_text, prompt)

            if summary:
                st.markdown("## Detailed Notes:")
                st.write(summary)
        else:
            st.warning("No transcript available for this video.")
