import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import re

st.set_page_config(page_title="Smart Notes Maker")

st.title("🎓 Smart Notes Maker")

url = st.text_input("YouTube link dalein:")

def get_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

if st.button("Notes Banayein"):
    video_id = get_video_id(url)

    if not video_id:
        st.error("❌ Invalid YouTube link")
    else:
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            # Pehle manual Hindi / English try
            try:
                transcript = transcript_list.find_manually_created_transcript(['hi', 'en'])
            except:
                transcript = transcript_list.find_generated_transcript(['hi', 'en'])

            captions = transcript.fetch()
            text = " ".join([i['text'] for i in captions])

            st.success("✅ Subtitles fetched successfully!")
            st.text_area("Transcript:", text, height=300)

        except TranscriptsDisabled:
            st.error("❌ Is video me captions disabled hain.")
        except NoTranscriptFound:
            st.error("❌ Is video me Hindi/English subtitles available nahi hain.")
        except Exception as e:
            st.error("⚠️ YouTube ne request block kar di (Cloud issue).")
