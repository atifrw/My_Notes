import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import re

st.set_page_config(page_title="EduNotes AI", page_icon="🎓", layout="centered")

# CSS for better mobile look
st.markdown("""<style>.main { background-color: #f0f2f5; } .stButton>button { width: 100%; border-radius: 10px; background: #1a73e8; color: white; }</style>""", unsafe_allow_html=True)

st.title("🎓 EduNotes AI")
video_url = st.text_input("YouTube URL yahan dalein:")

# Yahan humne key hatadi hai, ye ab 'Secrets' se aayegi
api_key = st.secrets.get("GEMINI_API_KEY")

def get_video_id(url):
    regex = r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^\"&?\/\s]{11})"
    match = re.search(regex, url)
    return match.group(1) if match else None

if st.button("Generate Notes ✨"):
    if not api_key:
        st.error("API Key missing! Streamlit ki Settings -> Secrets mein key dalein.")
    elif video_url:
        v_id = get_video_id(video_url)
        if v_id:
            try:
                with st.spinner('AI kaam kar raha hai...'):
                    transcript = YouTubeTranscriptApi.get_transcript(v_id)
                    text = " ".join([t['text'] for t in transcript])
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(f"Summarize this: {text}")
                    st.success("Aapke Notes Taiyar Hain!")
                    st.write(response.text)
            except Exception as e:
                st.error("Video mein captions band hain.")
        else:
            st.error("Invalid YouTube Link.")
