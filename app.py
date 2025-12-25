import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

st.set_page_config(page_title="EduNotes Pro")
st.title("🎓 Smart Notes Maker")

url = st.text_input("YouTube link dalein:")
key = st.secrets.get("GEMINI_API_KEY")

if st.button("Notes Banayein"):
    try:
        # Link se ID nikalne ka sabse simple tarika
        v_id = url.split("v=")[1].split("&")[0] if "v=" in url else url.split("/")[-1].split("?")[0]
        
        with st.spinner('Likh raha hoon...'):
            # Direct fetch
            data = YouTubeTranscriptApi.get_transcript(v_id)
            text = " ".join([t['text'] for t in data])
            
            genai.configure(api_key=key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            res = model.generate_content(f"Summarize this: {text}")
            st.write(res.text)
    except Exception as e:
        st.error("Bhai, YouTube ne block kiya hai ya subtitles nahi hain. Dusra video try karo.")
