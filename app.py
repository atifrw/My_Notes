import streamlit as st
import youtube_transcript_api
import google.generativeai as genai
import re

# Premium look settings
st.set_page_config(page_title="EduNotes Pro", page_icon="📝")

st.markdown("""
    <style>
    .main { background-color: #f0f2f5; }
    .stButton>button { background: #1a73e8; color: white; border-radius: 10px; font-weight: bold; width: 100%; height: 50px; }
    .note-card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); color: #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 Smart Notes Maker")
video_url = st.text_input("YouTube link dalein:")
api_key = st.secrets.get("GEMINI_API_KEY")

def get_id(url):
    regex = r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^\"&?\/\s]{11})"
    match = re.search(regex, url)
    return match.group(1) if match else None

if st.button("Notes Taiyar Karein ✨"):
    if video_url:
        v_id = get_id(video_url)
        if v_id:
            try:
                with st.spinner('AI notes bana raha hai...'):
                    # --- YAHAN HAI ASLI JADOO ---
                    # Hum sabse purana aur mazboot tarika use karenge jo kabhi fail nahi hota
                    from youtube_transcript_api import YouTubeTranscriptApi
                    data = YouTubeTranscriptApi.get_transcript(v_id, languages=['en', 'hi'])
                    full_text = " ".join([t['text'] for t in data])
                    
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(f"Summarize this lecture transcript in points: {full_text}")
                    
                    st.success("✅ Taiyar hai!")
                    st.markdown(f"<div class='note-card'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                # Agar video me subtitles nahi honge tabhi ye aayega
                st.error("Bhai, is video ke subtitles AI ko nahi mil rahe. Koi dusra video try karo.")
        else:
            st.error("Link galat hai bhai!")
    else:
        st.warning("Link toh dalo!")
