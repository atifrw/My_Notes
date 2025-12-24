import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

# Page Setup (Premium look ke liye)
st.set_page_config(page_title="EduNotes AI", page_icon="📝", layout="wide")

# Custom CSS for Premium Design
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { background-color: #4CAF50; color: white; border-radius: 10px; border: none; padding: 10px 24px; font-weight: bold; width: 100%; }
    .stTextInput>div>div>input { border-radius: 10px; border: 1px solid #ddd; }
    .header-style { color: #2c3e50; text-align: center; padding: 20px; font-family: 'Helvetica'; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='header-style'>🎓 AI Student Lecture Assistant</h1>", unsafe_allow_html=True)
st.write("---")

# User Input Section
col1, col2 = st.columns([2, 1])

with col1:
    video_url = st.text_input("YouTube Video URL yahan paste karein:")
with col2:
    # Yahan humne aapka API key fit kar diya hai (Secret rakhne ke liye baad mein ise hatayenge)
    api_key = "AIzaSyBGFT49_0fKLOHQNBTS3tX_cJhmOdMvqGE"

if st.button("Generate Magic Notes ✨"):
    if video_url:
        try:
            video_id = video_url.split("v=")[1].split("&")[0]
            with st.spinner('AI video ki gehraayi mein ja raha hai...'):
                # Transcript nikalna
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                transcript_text = " ".join([t['text'] for t in transcript_list])

                # AI Processing
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"""Tum ek world-class professor ho. Is video transcript se:
                1. Saaf Headings ke saath detailed 'Topper Style' Notes banao.
                2. Saare technical keywords ko bold karo.
                3. Ek 'Summary' aur 3 'Practice Questions' bhi add karo.
                Transcript: {transcript_text}"""
                
                response = model.generate_content(prompt)
                
                st.success("✅ Aapke Notes Taiyar Hain!")
                st.markdown(response.text)
        except Exception as e:
            st.error("Error: Is video ka transcript nahi mil raha ya link galat hai.")
    else:
        st.warning("Pehle YouTube link toh daaliye!")
