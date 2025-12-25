import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import re

# Layout Setup
st.set_page_config(page_title="EduNotes AI", page_icon="🎓", layout="centered")

# CSS for Clean Look
st.markdown("""<style>.main { background-color: #f8f9fa; } .stButton>button { width: 100%; border-radius: 10px; background: #007bff; color: white; height: 50px; border: none; font-weight: bold; }</style>""", unsafe_allow_html=True)

st.title("🎓 EduNotes AI")
st.write("YouTube Link dalein aur Notes taiyar karein.")

# Input
video_url = st.text_input("", placeholder="https://youtube.com/watch?v=...")

# --- SECRETS CONNECTION ---
# Ye line check karegi ki aapne settings me key dali hai ya nahi
api_key = st.secrets.get("GEMINI_API_KEY")

def get_video_id(url):
    regex = r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^\"&?\/\s]{11})"
    match = re.search(regex, url)
    return match.group(1) if match else None

if st.button("Generate Smart Notes ✨"):
    if not api_key:
        st.error("Error: API Key nahi mili! Settings -> Secrets mein 'GEMINI_API_KEY' dalein.")
    elif video_url:
        v_id = get_video_id(video_url)
        if v_id:
            try:
                with st.spinner('AI notes bana raha hai...'):
                    # 1. Transcript nikalna
                    transcript = YouTubeTranscriptApi.get_transcript(v_id)
                    text = " ".join([t['text'] for t in transcript])
                    
                    # 2. AI Process
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = f"Write detailed student notes for this: {text}"
                    response = model.generate_content(prompt)
                    
                    st.success("✅ Notes ready!")
                    st.markdown(response.text)
            except Exception as e:
                st.error("Is video me captions band hain ya koi technical error hai.")
        else:
            st.error("Galt YouTube Link hai.")
    else:
        st.warning("Pehle link toh daliye!")
