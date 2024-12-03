import streamlit as st
import yt_dlp as youtube_dl
import os

# Function to download video from YouTube using yt-dlp
def download_youtube_video(url, format_id, download_dir):
    try:
        ydl_opts = {
            'quiet': True,
            'format': format_id,
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            # Construct file path
            file_path = os.path.join(download_dir, f"{info_dict['title']}.{info_dict['ext']}")
            print(f"Downloaded file path: {file_path}")  # Debug print to verify path

            # Check if the file exists
            if os.path.exists(file_path):
                return file_path, f"{info_dict['title']}.{info_dict['ext']}"
            else:
                st.error("File not found after download!")
                print("File does not exist after download!")  # Debug print
                return None, None
    except Exception as e:
        st.error(f"Error: {e}")
        print(f"Exception occurred: {e}")  # Debug print
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

            # Choose a directory to save the video (e.g., a 'downloads' folder)
            download_dir = 'downloads'
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)

            # Download button
            if st.button("Download Video"):
                with st.spinner("Downloading..."):
                    file_path, file_name = download_youtube_video(url, selected_format_id, download_dir)
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
