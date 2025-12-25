import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import re

st.set_page_config(page_title="EduNotes AI", page_icon="🎓")

# Secret Key Check
api_key = st.secrets.get("GEMINI_API_KEY")

st.title("🎓 Smart Notes Maker")

video_url = st.text_input("YouTube Link Paste Karein:")

if st.button("Notes Banayein"):
    if video_url:
        # Video ID nikalne ka sabse mazboot tarika
        video_id = None
        if "v=" in video_url:
            video_id = video_url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in video_url:
            video_id = video_url.split("youtu.be/")[1].split("?")[0]

        if video_id:
            try:
                with st.spinner('Video padh raha hoon...'):
                    # Transcript lene ki koshish
                    transcript = YouTubeTranscriptApi.get_transcript(video_id)
                    text = " ".join([t['text'] for t in transcript])
                    
                    # AI Processing
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(f"Summarize this in Hindi-English mix: {text}")
                    
                    st.success("Taiyar hai!")
                    st.write(response.text)
            except Exception as e:
                # Ye line humein batayegi asli error kya hai
                st.error(f"Dikkat ye hai: {str(e)}")
        else:
            st.error("Link sahi se copy karein.")
