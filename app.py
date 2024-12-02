import streamlit as st
import yt_dlp as youtube_dl
import instaloader
import tempfile
import os

# Function to get available formats for YouTube using yt-dlp
def get_youtube_formats(url):
    try:
        ydl_opts = {
            'quiet': True,
            'extract_audio': False,  # Don't extract audio only
            'force_generic_extractor': False,
            'format': 'bestaudio/best',  # Best available audio/video
            'noplaylist': True,  # Don't download playlists
            'skip_download': True  # Skip actual download, just fetch formats
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=False)
            formats = result.get('formats', [])

            # Creating a list of available resolutions
            available_formats = []
            for f in formats:
                if 'format_note' in f:
                    available_formats.append((f['format_note'], f['format_id']))

            return available_formats
    except Exception as e:
        st.error(f"Error: {e}")
        return []

# Function to download video from YouTube using yt-dlp
def download_youtube_video(url, format_id):
    try:
        ydl_opts = {
            'quiet': True,  # Suppress logs
            'format': format_id,  # Select the specified format ID
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            ydl_opts['outtmpl'] = os.path.join(temp_dir, '%(title)s.%(ext)s')
            
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                file_path = os.path.join(temp_dir, f"{info_dict['title']}.{info_dict['ext']}")
                return file_path, info_dict['title']
    except Exception as e:
        st.error(f"Error: {e}")
        return None, None

# Function to download Instagram video/reel
def download_instagram_video(url):
    loader = instaloader.Instaloader()
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            loader.download_post(instaloader.Post.from_shortcode(loader.context, url.split("/")[-2]), target=temp_dir)
            video_file = [f for f in os.listdir(temp_dir) if f.endswith('.mp4')]

            if video_file:
                file_path = os.path.join(temp_dir, video_file[0])
                return file_path, video_file[0]
            else:
                st.error("No video file found in the post.")
                return None, None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, None

# Streamlit app interface
def main():
    st.title('YouTube & Instagram Video/Reel Downloader')

    # Select platform
    platform = st.selectbox("Choose a platform", ['YouTube', 'Instagram'])

    # Input URL
    url = st.text_input("Enter video URL")

    if platform == 'YouTube':
        if url:
            st.write("Fetching available resolutions...")
            available_formats = get_youtube_formats(url)

            if available_formats:
                # Display available formats to select from
                format_options = [f"{resolution} ({format_id})" for resolution, format_id in available_formats]
                selected_format = st.selectbox("Select format", format_options)

                # Extract the format_id from the selected option
                selected_format_id = available_formats[format_options.index(selected_format)][1]

                if st.button("Download Video"):
                    with st.spinner('Downloading...'):
                        file_path, file_name = download_youtube_video(url, selected_format_id)
                        if file_path:
                            with open(file_path, "rb") as file:
                                st.download_button(
                                    label="Download Video",
                                    data=file,
                                    file_name=file_name,
                                    mime="video/mp4"
                                )

    elif platform == 'Instagram':
        if url:
            if st.button("Download Video"):
                with st.spinner('Downloading...'):
                    file_path, file_name = download_instagram_video(url)
                    if file_path:
                        with open(file_path, "rb") as file:
                            st.download_button(
                                label="Download Video",
                                data=file,
                                file_name=file_name,
                                mime="video/mp4"
                            )

# Run the app
if __name__ == "__main__":
    main()