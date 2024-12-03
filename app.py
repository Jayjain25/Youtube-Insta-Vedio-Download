# import streamlit as st
# import yt_dlp as youtube_dl
# import instaloader
# import os

# # Function to get available formats for YouTube using yt-dlp
# def get_youtube_formats(url):
#     try:
#         ydl_opts = {
#             'quiet': True,
#             'extract_audio': False,  # Don't extract audio only
#             'force_generic_extractor': False,
#             'format': 'bestaudio/best',  # Best available audio/video
#             'noplaylist': True,  # Don't download playlists
#             'skip_download': True  # Skip actual download, just fetch formats
#         }
        
#         with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#             result = ydl.extract_info(url, download=False)
#             formats = result.get('formats', [])
            
#             # Creating a list of available resolutions
#             available_formats = []
#             for f in formats:
#                 if 'format_note' in f:
#                     available_formats.append((f['format_note'], f['format_id']))
            
#             return available_formats
#     except youtube_dl.DownloadError as e:
#         st.error(f"Error: Download error occurred - {e}")
#         return []
#     except youtube_dl.ExtractorError as e:
#         st.error(f"Error: Extractor error - {e}")
#         return []
#     except Exception as e:
#         st.error(f"An unexpected error occurred while fetching YouTube formats: {e}")
#         return []

# # Function to download video from YouTube using yt-dlp
# def download_youtube_video(url, format_id):
#     try:
#         ydl_opts = {
#             'quiet': False,  # Show logs for debugging
#             'format': format_id,  # Select the specified format ID
#             'outtmpl': 'downloads/%(title)s.%(ext)s',  # Download path and filename format
#             'noplaylist': True,  # Don't download playlists
#         }

#         with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#             info_dict = ydl.extract_info(url, download=True)
#             st.success(f"Downloaded: {info_dict['title']}")
#     except youtube_dl.DownloadError as e:
#         st.error(f"Error: Download error occurred - {e}")
#     except youtube_dl.ExtractorError as e:
#         st.error(f"Error: Extractor error - {e}")
#     except FileNotFoundError as e:
#         st.error(f"Error: File not found - {e}")
#     except Exception as e:
#         st.error(f"An unexpected error occurred while downloading the video: {e}")

# # Function to download Instagram video/reel
# def download_instagram_video(url):
#     loader = instaloader.Instaloader()
#     try:
#         post = loader.get_post(url, target='')
#         video_url = post.url  # Instagram post URL
#         st.video(video_url)   # You can play the video directly in the app
#         st.write(f"Download URL: {video_url}") # For direct download link
#     except instaloader.exceptions.InstaloaderException as e:
#         st.error(f"Error: Instagram download failed - {str(e)}")
#     except Exception as e:
#         st.error(f"An unexpected error occurred while downloading Instagram video: {e}")

# # Streamlit app interface
# def main():
#     st.title('YouTube & Instagram Video/ Reel Downloader')

#     # Select platform
#     platform = st.selectbox("Choose a platform", ['YouTube', 'Instagram'])

#     # Input URL
#     url = st.text_input("Enter video URL")

#     if platform == 'YouTube':
#         if url:
#             st.write("Fetching available resolutions...")
#             available_formats = get_youtube_formats(url)
            
#             if available_formats:
#                 # Display available formats to select from
#                 format_options = [f"{resolution} ({format_id})" for resolution, format_id in available_formats]
#                 selected_format = st.selectbox("Select format", format_options)
                
#                 # Extract the format_id from the selected option
#                 selected_format_id = available_formats[format_options.index(selected_format)][1]

#                 if st.button("Download Video"):
#                     with st.spinner('Downloading...'):
#                         download_youtube_video(url, selected_format_id)

#     elif platform == 'Instagram':
#         if url:
#             st.write("Fetching Instagram video/reel...")
#             download_instagram_video(url)

# # Run the app
# if __name__ == "__main__":
#     main()

import streamlit as st
import yt_dlp as youtube_dl
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
    except youtube_dl.DownloadError as e:
        st.error(f"Error: Download error occurred - {e}")
        return []
    except youtube_dl.ExtractorError as e:
        st.error(f"Error: Extractor error - {e}")
        return []
    except Exception as e:
        st.error(f"An unexpected error occurred while fetching YouTube formats: {e}")
        return []

# Function to download video from YouTube using yt-dlp
def download_youtube_video(url, format_id, download_path):
    try:
        # Set options for yt-dlp
        ydl_opts = {
            'quiet': True,
            'format': format_id,
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),  # Save to the local path
            'noplaylist': True,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = os.path.join(download_path, f"{info_dict['title']}.{info_dict['ext']}")
            st.success(f"Downloaded: {info_dict['title']} to {download_path}")
            
            # Return the file path for download link
            return file_path
    except youtube_dl.DownloadError as e:
        st.error(f"Error: Download error occurred - {e}")
    except youtube_dl.ExtractorError as e:
        st.error(f"Error: Extractor error - {e}")
    except FileNotFoundError as e:
        st.error(f"Error: File not found - {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred while downloading the video: {e}")

# Streamlit app interface
def main():
    st.title('YouTube Video Downloader')

    # Input URL
    url = st.text_input("Enter YouTube video URL")

    # Set a local download path
    download_path = os.path.expanduser('~/Downloads')  # This should be the default download directory

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
                    downloaded_file_path = download_youtube_video(url, selected_format_id, download_path)
                    if downloaded_file_path:
                        # Provide a download button for direct browser download
                        with open(downloaded_file_path, "rb") as file:
                            st.download_button(
                                label="Download Video",
                                data=file,
                                file_name=os.path.basename(downloaded_file_path),
                                mime="video/mp4"
                            )

# Run the app
if __name__ == "__main__":
    main()
