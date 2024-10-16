#
# This script splits a video file into multiple segments, each with a maximum length of 
# 4 1/2 minutes (270 seconds). It utilizes FFmpeg to handle video processing and 
# provides a user-friendly GUI for selecting both the input video file and the 
# output directory where the segments will be saved. 
#
# Key Features:
# - Detects the duration, resolution, audio codec, and bitrate of the input video.
# - Automatically generates unique filenames for output segments to prevent overwriting.
# - Logs all actions and errors to the console for easy tracking.
#
# Requirements:
# - FFmpeg and FFprobe must be installed and available in the system's PATH.
# - Python must have the necessary libraries (subprocess, logging, math, sys, tkinter).
#
# Usage:
# Run the script, select the input video file, choose the output directory, 
# and the script will create the segmented video files in the specified output location.



import os
import subprocess
import logging
import math
import sys
import tkinter as tk
from tkinter import filedialog

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def browse_file():
    """Opens a GUI file explorer to select the input video file."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select Video File",
        filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
    )
    if not file_path:
        logging.error("No file selected. Exiting.")
        sys.exit(1)
    return file_path

def browse_output_directory():
    """Opens a GUI file explorer to select the output directory."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    dir_path = filedialog.askdirectory(title="Select Output Directory")
    if not dir_path:
        logging.error("No output directory selected. Exiting.")
        sys.exit(1)
    return dir_path

def get_video_duration(input_file):
    """Returns the duration of the video in seconds."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", input_file],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    return float(result.stdout.strip())

def get_video_resolution(input_file):
    """Returns the resolution of the video."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", input_file],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    return result.stdout.strip()

def get_audio_codec(input_file):
    """Returns the audio codec of the input video."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=codec_name", "-of", "default=noprint_wrappers=1:nokey=1", input_file],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    return result.stdout.strip()

def get_bitrate(input_file):
    """Returns the video bitrate in bits per second."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "format=bit_rate", "-of", "default=noprint_wrappers=1:nokey=1", input_file],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    return int(result.stdout.strip())

def generate_unique_filename(output_file):
    """Generates a unique filename if the file already exists."""
    base, ext = os.path.splitext(output_file)
    counter = 1
    while os.path.exists(output_file):
        output_file = f"{base}_{counter}{ext}"
        counter += 1
    return output_file

def split_video(input_file, output_directory, segment_length=270):
    """Splits the input video into segments with the given length in seconds."""
    try:
        total_duration = get_video_duration(input_file)
        num_segments = math.ceil(total_duration / segment_length)
        resolution = get_video_resolution(input_file)
        audio_codec = get_audio_codec(input_file)
        bitrate = get_bitrate(input_file)
        
        logging.info(f"Total video duration: {total_duration:.2f} seconds.")
        logging.info(f"Splitting into {num_segments} segments.")
        logging.info(f"Video Resolution: {resolution}")
        logging.info(f"Audio Codec: {audio_codec}")
        logging.info(f"Video Bitrate: {bitrate} bps")
        
        for i in range(num_segments):
            start_time = i * segment_length
            output_file = os.path.join(output_directory, f"segment_{i + 1}.mp4")
            output_file = generate_unique_filename(output_file)  # Ensure unique filename
            logging.info(f"Processing segment {i + 1}/{num_segments}, Start Time: {start_time} seconds")
            
            command = [
                "ffmpeg", "-i", input_file, "-ss", str(start_time), "-t", str(segment_length),
                "-c", "copy", "-avoid_negative_ts", "1", output_file
            ]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            if result.returncode != 0:
                logging.error(f"Error creating segment {i + 1}: {result.stderr}")
                sys.exit(1)
            else:
                logging.info(f"Segment {i + 1} saved as {output_file}")

        logging.info("Video splitting completed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Subprocess error: {e.stderr}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    input_file = browse_file()
    output_directory = browse_output_directory()
    split_video(input_file, output_directory)
