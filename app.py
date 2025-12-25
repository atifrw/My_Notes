import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import re

# Page Setup - Mobile responsive layout
st.set_page_config(page_title="EduNotes Pro", page_icon="🎓", layout="centered")

# Custom CSS for a Mobile App-like Premium Look
st.markdown("""
    <style>
    /* Background and Font */
    .main { background: #f0f2f5; }
    
    /* Title Styling */
    .title { color: #1e3a8a; text-align: center; font-size: 24px; font-weight: 800; margin-bottom: 5px; }
    .subtitle { color: #64748b; text-align: center; font-size: 14px; margin-bottom: 25px; }

    /* Input Box Styling */
    .stTextInput input {
        border-radius: 12px !important;
        border: 2px solid #d1d5db !important;
        padding: 12px !important;
    }

    /* Button Styling - Premium Gradient */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 15px;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Result Card */
    .note-card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-top: 20px;
        color: #1f2937;
    }
    </style>
    """, unsafe_allow_html=True)

# UI Elements
st.markdown("<div class='title'>🎓 EduNotes Pro AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>YouTube Lecture ko Smart Notes mein badlein</div>", unsafe_allow_html=True)

# Input Field
video_url = st.text_input("", placeholder="YouTube link yahan paste karein...")

# Hidden Sidebar for API Key
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Gemini API Key", type="password", value="AIzaSyBGFT49_0fKLOHQNBTS3tX_cJhmOdMvqGE")

def get_video_id(url):
    # Regex to handle all types of YT links (Shorts, Mobile, Desktop)
    regex = r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^\"&?\/\s]{11})"
    match = re.search(regex, url)
    return match.group(1) if match else None

if st.button("Generate Smart Notes ✨"):
    if video_url:
        v_id = get_video_id(video_url)
        if v_id:
            try:
                with st.spinner('🤖 AI Notes taiyar kar raha hai...'):
                    # Fetching Transcript
                    transcript_data = YouTubeTranscriptApi.get_transcript(v_id)
                    full_text = " ".join([t['text'] for t in transcript_data])

                    # AI Setup
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = f"Tum ek expert topper ho. Is lecture transcript se saaf-sutre study notes banao. Bullet points ka use karo aur important terms ko Bold karo. Transcript: {full_text}"
                    
                    response = model.generate_content(prompt)
                    
                    # Displaying Output
                    st.balloons()
                    st.markdown("### 📝 Aapke Notes:")
                    st.markdown(f"<div class='note-card'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error("❌ Is video mein captions available nahi hain.")
        else:
            st.error("❌ Link sahi nahi hai. Kripya sahi YouTube URL dalein.")
    else:
        st.warning("Pehle link toh daaliye!")
