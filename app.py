import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import re

# Premium Mobile-First Layout
st.set_page_config(page_title="EduNotes AI", page_icon="🎓", layout="centered")

# Custom Styling taaki website "Ghatiya" na lage
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stTextInput input { border-radius: 8px !important; border: 1px solid #ddd !important; padding: 10px !important; }
    .stButton>button { 
        background: #000000; color: white; border-radius: 8px; 
        font-weight: bold; width: 100%; height: 45px; border: none;
    }
    .note-box { background: #f9f9f9; padding: 20px; border-radius: 12px; border-left: 5px solid #000; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 Smart Notes Maker")
st.write("Apna YouTube link niche dalein:")

# Input Field
video_url = st.text_input("", placeholder="https://youtu.be/...")

# API Key from Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

def get_id(url):
    regex = r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^\"&?\/\s]{11})"
    match = re.search(regex, url)
    return match.group(1) if match else None

if st.button("Magic Notes Generate Karein ✨"):
    if video_url:
        v_id = get_id(video_url)
        if v_id:
            try:
                with st.spinner('🤖 AI Video ko padh raha hai...'):
                    # ERROR FIX: Function name sahi kar diya hai
                    transcript_list = YouTubeTranscriptApi.list_transcripts(v_id)
                    transcript = transcript_list.find_transcript(['en', 'hi'])
                    data = transcript.fetch()
                    full_text = " ".join([t['text'] for t in data])
                    
                    # AI Magic
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(f"Create professional student notes from this: {full_text}")
                    
                    st.success("Done!")
                    st.markdown(f"<div class='note-box'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error("Is video mein captions/subtitles band hain. Koi dusra video try karein.")
        else:
            st.error("Link sahi nahi hai.")
    else:
        st.warning("Pehle link toh daliye!")
