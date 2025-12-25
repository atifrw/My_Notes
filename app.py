try:
    with st.spinner('Extraction shuru hai...'):
        # Sabse pehle saari available transcripts ki list check karein
        transcript_list_obj = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # English ya Hindi dhoondne ki koshish karein (Manually ya Auto-generated dono)
        try:
            # Pehle manually likhe hue captions check karein
            transcript = transcript_list_obj.find_transcript(['en', 'hi'])
        except:
            # Agar manual nahi hai, toh auto-generated (translated) uthayein
            transcript = transcript_list_obj.find_generated_transcript(['en', 'hi'])

        data = transcript.fetch()
        full_transcript = " ".join([item['text'] for item in data])
        
        st.success("Mil gaya!")
        st.text_area("Result:", full_transcript, height=300)
        
except Exception as e:
    st.error("Error: YouTube ne access block kiya hai ya subtitles available nahi hain.")
    st.info("Tip: Kuch videos par 'Auto-generated' subtitles hote hain jo kabhi-kabhi block hote hain.")
    
