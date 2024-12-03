import yt_dlp as youtube_dl
import os
import streamlit as st

# Function to download a YouTube video
def download_youtube_video(url, format_id):
    try:
        # Use the current working directory as the default download directory
        download_dir = os.getcwd()
        ydl_opts = {
            'quiet': True,
            'format': format_id,
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
            'progress_hooks': [show_progress],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = os.path.join(download_dir, f"{info_dict['title']}.{info_dict['ext']}")
            
            # Check if the file was downloaded successfully
            if os.path.exists(file_path):
                st.success(f"File downloaded successfully: {file_path}")
                return file_path
            else:
                st.error("Error: File not found after download!")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Function to display download progress
def show_progress(d):
    if d['status'] == 'downloading':
        percent = d['downloaded_bytes'] / d['total_bytes'] * 100
        st.progress(percent)

# Main Streamlit app
def main():
    st.title("YouTube Video Downloader")

    url = st.text_input("Enter YouTube video URL:")

    if st.button("Get Available Formats"):
        if url:
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

            if available_formats:
                format_options = [f"{res} ({fid})" for res, fid in available_formats]
                selected_format = st.selectbox("Select format:", format_options)

                if st.button("Download Video"):
                    selected_format_id = [fid for res, fid in available_formats if f"{res} ({fid})" == selected_format][0]
                    file_path = download_youtube_video(url, selected_format_id)
                    if file_path:
                        st.write(f"Download complete. File saved to: {file_path}")
                        # Optionally add a link to download the file
                        st.download_button("Download File", file_path)
            else:
                st.warning("No available formats found.")
        else:
            st.warning("Please enter a valid YouTube URL.")

if __name__ == "__main__":
    main()
