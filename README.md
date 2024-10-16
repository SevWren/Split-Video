# Video Splitter Script

This Python script allows you to split a video file into multiple segments, each with a maximum length of 4 1/2 minutes (270 seconds).  
It leverages **FFmpeg** for video processing and provides a graphical user interface (GUI) for selecting the input video file and the output directory where the segments will be saved.

---

## Future Plans

- Add manual time selection
- Add split by size limit
- Support for multiple video formats
- Support for only audio formats
- Logging to custom log file locations

---

## Key Features

- **Detection:** Automatically detects the duration, resolution, audio codec, and bitrate of the input video.
- **Unique Filenames:** Generates unique filenames for output segments to prevent overwriting existing files.
- **Logging:** Logs all actions and errors to the console for easy tracking.
- **User-Friendly GUI:** Simplifies file selection and output folder choice.

---

## Requirements

- **Python 3.x**: Ensure you have Python installed on your machine.
- **FFmpeg**: Install FFmpeg and make sure it is available in your system's PATH. You can download it from [FFmpeg's official website](https://ffmpeg.org/download.html).
- **Required Python Libraries**: The script uses the following libraries:
  - `subprocess`
  - `logging`
  - `math`
  - `sys`
  - `tkinter`

---

## Usage

1. Clone this repository or download the script files to your local machine.
2. Ensure FFmpeg is installed and added to your system PATH.
3. Open a terminal or command prompt.
4. Navigate to the directory containing the script.
5. Run the script with the following command:

   ```bash
   python split_video.py
