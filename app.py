def add_local_video(video_path, title, caption):
    """Add local video with custom styling"""
    try:
        # Read video file
        with open(video_path, 'rb') as video_file:
            video_bytes = video_file.read()
        
        # Create styled container
        st.markdown(f"""
        <div class="video-container" style="margin: 20px 0; padding: 15px; background: linear-gradient(135deg, #FF1E1E 0%, #FF6B6B 100%); 
                    border-radius: 15px; color: white;">
            <h4 style="margin-bottom: 15px; text-align: center;">{title}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Display video using Streamlit's native function
        st.video(video_bytes)
        
        # Add caption
        st.markdown(f"""
        <div style="text-align: center; margin-top: 10px;">
            <p style="font-size: 0.9rem; color: #666; opacity: 0.9;">{caption}</p>
        </div>
        """, unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.error(f"❌ Video file not found: {video_path}")
        st.info("💡 Please ensure the video file exists at the specified path")
    except Exception as e:
        st.error(f"❌ Error loading video: {str(e)}")

def add_youtube_video(video_id, title, caption):
    """Add YouTube video with custom styling"""
    st.markdown(f"""
    <div class="video-container" style="margin: 20px 0; padding: 15px; background: linear-gradient(135deg, #FF1E1E 0%, #FF6B6B 100%); 
                border-radius: 15px; color: white;">
        <h4 style="margin-bottom: 15px; text-align: center;">{title}</h4>
        <div style="position: relative; width: 100%; height: 0; padding-bottom: 56.25%;">
            <iframe src="https://www.youtube.com/embed/{video_id}" 
                    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 10px;"
                    frameborder="0" allowfullscreen>
            </iframe>
        </div>
        <p style="margin-top: 15px; font-size: 0.9rem; text-align: center; opacity: 0.9;">{caption}</p>
    </div>
    """, unsafe_allow_html=True)
