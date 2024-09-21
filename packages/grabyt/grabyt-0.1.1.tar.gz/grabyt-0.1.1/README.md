# Video Downloader CLI

A command-line application for downloading videos and audio using `yt-dlp`. This tool supports multiple formats and resolutions, allowing you to save videos and extract audio easily.

## Features

- Download videos in various resolutions (1080p, 480p)
- Extract audio and save it as MP3
- Simple command-line interface with rich prompts
- Uses `yt-dlp` for powerful video downloading capabilities
- FFmpeg integration for audio processing

## Prerequisites

Before using this application, ensure you have the following installed:

- **Python 3.12** or later
- **FFmpeg** (used for audio extraction)
  - **Ubuntu/Debian**: 
    ```bash
    sudo apt install ffmpeg
    ```
  - **macOS** (using Homebrew): 
    ```bash
    brew install ffmpeg
    ```
  - **Windows**: Download the FFmpeg binaries from [FFmpeg's official website](https://ffmpeg.org/download.html) and add the path to your system's `PATH` variable.

## Installation

You can install this package via pip:

```bash
pip install your_package_name
```

## Usage

To use the Video Downloader CLI, simply run

```bash
ytdl
``` 

You will be prompted to enter the video URL and select the desired format. The available options are:
    1080p: Download the best video with a maximum height of 1080 pixels.
    480p: Download the best video with a maximum height of 480 pixels.
    Mp3: Extract the best audio and save it as an MP3 file.


## Example

Run the application:

```bash
ytdl
```
Enter the video URL when prompted.
Select the desired resolution or audio option.
The video or audio file will be downloaded to the current directory.


### License
This project is licensed under the MIT License - see the LICENSE file for details.
Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## Contact
For questions or feedback, feel free to reach out:
- Author: Muhammad Noman
- Email: mhmdnoman01@gmail.com
- X: https://x.com/BitWizCoder 

