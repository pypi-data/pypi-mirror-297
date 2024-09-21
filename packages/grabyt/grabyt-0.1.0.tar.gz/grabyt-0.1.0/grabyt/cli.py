import typer
import yt_dlp
from rich.prompt import Prompt
from rich.console import Console

console = Console()
app = typer.Typer()

FORMATS = {
    "1080p": "bestvideo[height<=1080]+bestaudio/best",
    "480p": 'bestvideo[height<=480]+bestaudio/best[height<=480]',
    "Mp3": "bestaudio",  # Use 'bestaudio' to select the best audio stream
}

@app.command()
def download_video():
    url = Prompt.ask("Enter the video URL")
    
    console.print("\nSelect a resolution:")
    for i, (resolution, _) in enumerate(FORMATS.items(), 1):
        console.print(f"{i}. {resolution}")
    
    choice = Prompt.ask("\nEnter your choice", choices=[str(i) for i in range(1, len(FORMATS) + 1)])
    selected_format = list(FORMATS.values())[int(choice) - 1]

    # Initialize YoutubeDL options
    ydl_opts = {
        'format': selected_format,
        'outtmpl': '%(title)s.%(ext)s',  # Output file name format
    }

    # If the user selects 'Mp3', add specific options for audio extraction
    if selected_format == "bestaudio":
        ydl_opts.update({
            'format': 'bestaudio/best',   # Download the best available audio
            'postprocessors': [{          # Add postprocessing steps
                'key': 'FFmpegExtractAudio',  # Extract audio with ffmpeg
                'preferredcodec': 'mp3',      # Convert audio to mp3
                'preferredquality': '192',    # Set audio quality to 192 kbps
            }],
        })

    # Download the video or audio using yt-dlp Python API
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main():
    app()

if __name__ == "__main__":
    main()
