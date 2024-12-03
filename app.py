import yt_dlp as youtube_dl
import os

# Function to download a YouTube video
def download_youtube_video(url, format_id, download_dir):
    try:
        ydl_opts = {
            'quiet': True,
            'format': format_id,
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = os.path.join(download_dir, f"{info_dict['title']}.{info_dict['ext']}")
            print(f"Downloaded file path: {file_path}")  # Print for confirmation

            if os.path.exists(file_path):
                print(f"File downloaded successfully: {file_path}")
            else:
                print("Error: File not found after download!")
    except Exception as e:
        print(f"An error occurred: {e}")

# Main function for user input
def main():
    url = input("Enter YouTube video URL: ")
    download_dir = input("Enter download directory (or press Enter for current directory): ")
    if not download_dir:
        download_dir = os.getcwd()  # Default to the current working directory

    # Fetch available formats
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
        print("Available formats:")
        for i, (res, fid) in enumerate(available_formats):
            print(f"{i + 1}: {res} ({fid})")

        choice = int(input("Select format by number: ")) - 1
        if 0 <= choice < len(available_formats):
            selected_format_id = available_formats[choice][1]
            download_youtube_video(url, selected_format_id, download_dir)
        else:
            print("Invalid choice.")
    else:
        print("No available formats found.")

if __name__ == "__main__":
    main()
