import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import re

# Page Setup - Premium Mobile Look
st.set_page_config(page_title="EduNotes AI", page_icon="🎓", layout="centered")

# Custom CSS for App-like Feel
st.markdown("""
    <style>
    .main { background-color: #f0f2f5; }
    .stTextInput input { border-radius: 10px; padding: 12px; }
    .stButton>button { 
        background: #1a73e8; color: white; border-radius: 10px; 
        font-weight: bold; width: 100%; height: 50px; border: none;
    }
    .status-box { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 EduNotes AI")
st.write("Video link dalein aur notes payein.")

# Input Field
video_url = st.text_input("", placeholder="YouTube URL yahan paste karein...")

# --- SECRET KEY MANAGEMENT ---
# Hum key ab Streamlit ki settings se uthayenge
api_key = st.secrets.get("GEMINI_API_KEY")

def get_video_id(url):
    regex = r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^\"&?\/\s]{11})"
    match = re.search(regex, url)
    return match.group(1) if match else None

if st.button("Generate Smart Notes ✨"):
    if not api_key:
        st.error("Setup incomplete: API Key nahi mili. (Settings mein check karein)")
    elif video_url:
        v_id = get_video_id(video_url)
        if v_id:
            try:
                with st.spinner('🤖 AI Notes taiyar kar raha hai...'):
                    transcript = YouTubeTranscriptApi.get_transcript(v_id)
                    text = " ".join([t['text'] for t in transcript])
                    
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = f"Summarize this lecture into neat student notes with headings and bullet points: {text}"
                    response = model.generate_content(prompt)
                    
                    st.success("✅ Done!")
                    st.markdown(f"<div class='status-box'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error("Video mein captions band hain ya link sahi nahi hai.")
