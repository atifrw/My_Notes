import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="EduNotes Pro AI", page_icon="🚀", layout="wide")

# Premium CSS for modern look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    .main { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .stButton>button {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        color: white; border: none; border-radius: 12px;
        padding: 15px; font-size: 18px; font-weight: bold;
        transition: 0.3s; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.15); }
    .card {
        background: white; padding: 25px; border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05); margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Header Section
st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>🚀 EduNotes Pro AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>Video ko Smart Study Notes mein badlein - Topper ki tarah!</p>", unsafe_allow_html=True)

# Main Interface
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    video_url = st.text_input("🔗 YouTube Lecture Link Yahan Paste Karein", placeholder="https://youtube.com/watch?v=...")
    
    # Sidebar for API Key (Safety)
    with st.sidebar:
        st.title("⚙️ Settings")
        api_key = st.text_input("Gemini API Key dalein", type="password", value="AIzaSyBGFT49_0fKLOHQNBTS3tX_cJhmOdMvqGE")
        st.info("Aapki key yahan safe hai.")
    
    generate_btn = st.button("Generate Smart Notes ✨")
    st.markdown('</div>', unsafe_allow_html=True)

if generate_btn:
    if video_url:
        try:
            video_id = video_url.split("v=")[1].split("&")[0]
            with st.spinner('🤖 AI Video ko scan kar raha hai...'):
                # Transcript
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                text = " ".join([t['text'] for t in transcript])

                # AI Magic
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"Tum ek world-class tutor ho. Is lecture transcript se 'Professional Study Notes' banao jisme: 1. Executive Summary 2. Detailed Key Concepts (Bullet points) 3. Important Formulas/Dates 4. Quiz Questions. Transcript: {text}"
                
                response = model.generate_content(prompt)
                
                # Output
                st.balloons()
                st.markdown("### 📝 Aapke Exclusive Notes")
                st.markdown(f'<div class="card">{response.text}</div>', unsafe_allow_html=True)
                
                # Download Button (Optional)
                st.download_button("Download Notes (TXT)", response.text, file_name="notes.txt")
        except Exception as e:
            st.error("❌ Is video mein captions nahi hain ya link galat hai.")
    else:
        st.warning("Pehle link toh daliye!")
