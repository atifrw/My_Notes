import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import re

# Page Setup
st.set_page_config(page_title="EduNotes Pro", page_icon="📝")

# Design ko sudhara (Dark Mode Look)
st.markdown("""
    <style>
    .main { background-color: #121212; color: white; }
    .stTextInput>div>div>input { background-color: #1e1e1e; color: white; border-radius: 8px; }
    .stButton>button { background: #007bff; color: white; border-radius: 8px; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 Smart Notes Maker")

# URL Input
video_url = st.text_input("YouTube link yahan dalein:")

# Secret Key (Jo aapne Settings mein daali hai)
api_key = st.secrets.get("GEMINI_API_KEY")

def get_video_id(url):
    regex = r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^\"&?\/\s]{11})"
    match = re.search(regex, url)
    return match.group(1) if match else None

if st.button("Notes Taiyar Karein ✨"):
    if video_url:
        v_id = get_video_id(video_url)
        if v_id:
            try:
                with st.spinner('AI video ki gehraayi mein ja raha hai...'):
                    # --- YAHAN FIX HAI ---
                    # Ye pehle English, phir Hindi, phir Auto-generated subtitles check karega
                    try:
                        transcript_list = YouTubeTranscriptApi.list_transcripts(v_id)
                        transcript = transcript_list.find_transcript(['en', 'hi'])
                        data = transcript.fetch()
                    except:
                        # Agar upar wala fail ho jaye, toh koi bhi available transcript utha lo
                        transcript_list = YouTubeTranscriptApi.list_transcripts(v_id)
                        # Manual ya Auto-generated jo bhi pehla miley
                        for t in transcript_list:
                            data = t.fetch()
                            break
                    
                    full_text = " ".join([t['text'] for t in data])

                    # AI Setup
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = f"Bhai is transcript se mast detailed notes bana de: {full_text}"
                    response = model.generate_content(prompt)

                    st.success("✅ Notes ready hain!")
                    st.markdown(response.text)
                    
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Bhai link toh sahi se copy kar!")
    else:
        st.warning("Link toh daalo pehle!")
