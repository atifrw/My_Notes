import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import re

# Premium Mobile Look
st.set_page_config(page_title="EduNotes Pro", page_icon="📝")

st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stButton>button { background: #2ecc71; color: white; border-radius: 10px; width: 100%; font-weight: bold; height: 50px; }
    .note-card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); color: #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 Smart Notes Maker")

video_url = st.text_input("YouTube link yahan dalein:")
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
                with st.spinner('AI video ko scan kar raha hai...'):
                    # --- SABSE ZAROORI FIX YAHAN HAI ---
                    # Hum direct class use karenge bina galti ke
                    try:
                        # Pehle auto-generate ya manual transcript dhundne ki koshish
                        transcript_list = YouTubeTranscriptApi.list_transcripts(v_id)
                        transcript = transcript_list.find_transcript(['en', 'hi'])
                        data = transcript.fetch()
                    except:
                        # Agar upar wala na miley, toh jo bhi available ho wo utha lo
                        transcript_list = YouTubeTranscriptApi.list_transcripts(v_id)
                        for t in transcript_list:
                            data = t.fetch()
                            break
                    
                    full_text = " ".join([t['text'] for t in data])

                    # AI Setup
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = f"Summarize this lecture in clean student notes with headings: {full_text}"
                    response = model.generate_content(prompt)

                    st.balloons()
                    st.markdown("### 📝 Aapke Notes:")
                    st.markdown(f"<div class='note-card'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Bhai, ye error aa raha hai: {str(e)}")
        else:
            st.error("Link sahi se copy karo bhai!")
    else:
        st.warning("Pehle link toh daalo!")
