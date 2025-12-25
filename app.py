import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import re

st.set_page_config(page_title="EduNotes Pro", page_icon="📝")

st.title("🎓 Smart Notes Maker")

# Input
video_url = st.text_input("YouTube link dalein:")
api_key = st.secrets.get("GEMINI_API_KEY")

if st.button("Notes Taiyar Karein ✨"):
    if video_url:
        # Video ID nikalna
        v_id = None
        if "v=" in video_url: v_id = video_url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in video_url: v_id = video_url.split("youtu.be/")[1].split("?")[0]
        
        if v_id:
            try:
                with st.spinner('AI kaam kar raha hai...'):
                    # Direct fetch (Simple and Strong)
                    data = YouTubeTranscriptApi.get_transcript(v_id)
                    full_text = " ".join([t['text'] for t in data])
                    
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(f"Detailed study notes in points: {full_text}")
                    
                    st.success("Taiyar hai!")
                    st.write(response.text)
            except Exception as e:
                st.error("Error: Is video mein subtitles band hain.")
        else:
            st.error("Link sahi nahi hai.")
