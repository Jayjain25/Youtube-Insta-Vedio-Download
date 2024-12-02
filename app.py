import streamlit as st
import yt_dlp as youtube_dl
import tempfile
import os

# Function to download video from YouTube using yt-dlp
def download_youtube_video(url, format_id):
    try:
        ydl_opts = {
            'quiet': True,
            'format': format_id,
        }

        # Create a temporary directory for the file
        with tempfile.TemporaryDirectory() as temp_dir:
            ydl_opts['outtmpl'] = os.path.join(temp_dir, '%(title)s.%(ext)s')
            
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                file_path = os.path.join(temp_dir, f"{info_dict['title']}.{info_dict['ext']}")
                
                # Check if the file exists
                if os.path.exists(file_path):
                    return file_path, f"{info_dict['title']}.{info_dict['ext']}"
                else:
                    st.error("File not found after download!")
                    return None, None
    except Exception as e:
        st.error(f"Error: {e}")
        return None, None

# Streamlit app interface
def main():
    st.title('YouTube Video Downloader (Mobile Friendly)')

    # Input YouTube video URL
    url = st.text_input("Enter YouTube video URL")
    
    if url:
        # Fetch available formats
        st.write("Fetching available resolutions...")
        ydl_opts = {
            'quiet': True,
            'extract_audio': False,
            'format': 'best',
            'skip_download': True,
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=False)
            formats = result.get('formats', [])
        
        available_formats = [(f['format_note'], f['format_id']) for f in formats if 'format_note' in f]
        format_options = [f"{res} ({fid})" for res, fid in available_formats]
        
        if available_formats:
            # Let user choose the format
            selected_format = st.selectbox("Select format", format_options)
            selected_format_id = available_formats[format_options.index(selected_format)][1]

            # Download button
            if st.button("Download Video"):
                with st.spinner("Downloading..."):
                    file_path, file_name = download_youtube_video(url, selected_format_id)
                    if file_path:
                        # Provide file for download in browser
                        with open(file_path, "rb") as file:
                            st.download_button(
                                label="Download Video",
                                data=file,
                                file_name=file_name,
                                mime="video/mp4"
                            )

if __name__ == "__main__":
    main()
