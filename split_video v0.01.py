import subprocess
import math
import os
import logging
import sys

# Configure logging to display messages on screen and in case of errors
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Input video file
input_file = 'input.mp4'

# Maximum length per segment (in seconds)
max_length = 4 * 60 + 30  # 4 minutes and 30 seconds

# Helper function to run FFprobe commands and extract data
def ffprobe_info(file, stream_type, entry):
    try:
        command = [
            'ffprobe', '-v', 'error', '-select_streams', stream_type,
            '-show_entries', f'stream={entry}', '-of', 'default=noprint_wrappers=1:nokey=1', file
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        result.check_returncode()
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to retrieve {entry} from {stream_type}: {e}")
        sys.exit(1)

# Function to get video duration
def get_video_duration(file):
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', file],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        result.check_returncode()
        return float(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to retrieve video duration: {e}")
        sys.exit(1)

# Functions to extract properties
def get_video_resolution(file):
    width = ffprobe_info(file, 'v:0', 'width')
    height = ffprobe_info(file, 'v:0', 'height')
    return f"{width}x{height}"

def get_audio_codec(file):
    return ffprobe_info(file, 'a:0', 'codec_name')

def get_bitrate(file):
    return ffprobe_info(file, 'v:0', 'bit_rate')

# Main logic to split the video
def split_video():
    try:
        # Calculate total duration and number of segments
        total_duration = get_video_duration(input_file)
        num_segments = math.ceil(total_duration / max_length)
        logging.info(f"Total video duration: {total_duration:.2f} seconds.")
        logging.info(f"Splitting into {num_segments} segments.")

        # Create output directory if it doesn't exist
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        # Log the video properties
        logging.info(f"Video Resolution: {get_video_resolution(input_file)}")
        logging.info(f"Audio Codec: {get_audio_codec(input_file)}")
        logging.info(f"Video Bitrate: {get_bitrate(input_file)} bps")

        # Split video into segments
        for i in range(num_segments):
            start_time = i * max_length
            output_file = f"{output_dir}/segment_{i + 1}.mp4"
            logging.info(f"Processing segment {i + 1}/{num_segments}, Start Time: {start_time} seconds")

            result = subprocess.run([
                'ffmpeg', '-i', input_file, '-ss', str(start_time), '-t', str(max_length),
                '-c:v', 'copy', '-c:a', 'copy', '-b:v', get_bitrate(input_file),
                output_file
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode != 0:
                logging.error(f"Error creating segment {i + 1}: {result.stderr}")
            else:
                logging.info(f"Segment {i + 1} saved as {output_file}")

        logging.info("Video splitting completed successfully.")

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

# Run the script
if __name__ == "__main__":
    if not os.path.exists(input_file):
        logging.error(f"Input file '{input_file}' not found.")
        sys.exit(1)
    split_video()
