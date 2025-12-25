import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import re

# Page Configuration (Professional Look)
st.set_page_config(page_title="TranscribeYT - YouTube to Text", page_icon="📝", layout="centered")

# Custom CSS for Professional Styling
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #2563eb;
        color: white;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# Header Section
st.title("🎥 YouTube to Transcript")
st.markdown("Kisi bhi YouTube video ka URL niche daalein aur uska text turant nikaalein.")

# Function to extract Video ID
def extract_video_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# Input Area
url = st.text_input("YouTube Video Link", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Generate Transcript"):
    if url:
        video_id = extract_video_id(url)
        if video_id:
            try:
                with st.spinner('Extraction shuru hai...'):
                    # Fetching Transcript
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi', 'en'])
                    
                    # Joining text
                    full_transcript = " ".join([item['text'] for item in transcript_list])
                    
                    st.success("Success! Transcript niche di gayi hai:")
                    st.text_area("Result:", full_transcript, height=300)
                    
                    # Download Button
                    st.download_button("Download as Text File", full_transcript, file_name="transcript.txt")
                    
            except Exception as e:
                st.error(f"Error: Is video ke liye transcript available nahi hai. (Video settings check karein)")
        else:
            st.warning("Kripya sahi YouTube URL daalein.")
    else:
        st.info("Pahle URL enter karein.")

st.markdown("---")
st.caption("Developed for Content Creators | Powered by Streamlit")
