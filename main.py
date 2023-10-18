import os
import subprocess

# Directory containing video and audio files
input_directory = '/Users/andreidenisenko/Documents/Movies'

# Directory to store the merged and converted output
output_directory = '/Users/andreidenisenko/Documents/Movies/converted'

# Ensure the output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)


# Convert using NVIDIA GPU acceleration (hevc_nvenc) to H.265 with stereo audio
def convert_with_gpu(input_file, output_file):
    try:
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-c:v', 'hevc_nvenc',
            '-c:a', 'aac',
            '-ac', '2',
            '-strict', 'experimental',
            output_file
        ]
        subprocess.run(cmd)
    except Exception as e:
        print(f"Error converting file {input_file}. Error: {e}")

def handle_external_audio():
    # Check if there's a corresponding audio file with the same base name
    base_name = os.path.splitext(file)[0]
    audio_file = None

    # Check common audio extensions; you can expand this list
    for ext in ['.mp3', '.aac', '.wav', '.flac', '.ac3']:
        potential_audio_path = os.path.join(root, base_name + ext)
        if os.path.exists(potential_audio_path):
            audio_file = potential_audio_path
            break

    if audio_file:
        input_video = os.path.join(root, file)
        temp_output = os.path.join(output_directory, base_name + "_temp.mkv")

        # Merging command
        cmd_merge = [
            'ffmpeg',
            '-i', input_video,
            '-i', audio_file,
            '-c:v', 'copy',  # Copy video codec without re-encoding
            '-c:a', 'copy',  # Copy audio codec without re-encoding
            '-strict', 'experimental',
            temp_output
        ]

        # Run the merging command
        subprocess.run(cmd_merge)
        print(f"Merged {input_video} and {audio_file} to {temp_output}")

        # Final output after conversion
        final_output = os.path.join(output_directory, base_name + "_converted.mkv")
        return


for root, dirs, files in os.walk(input_directory):
    for file in files:
        # Check for video file extensions (you can extend this list as needed)
        try:
            if file.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):
                print(f"working on {file}")
                input_file = os.path.join(root, file)
                output_file = os.path.join(output_directory, os.path.splitext(file)[0] + '.mp4')

                # Conversion command
                cmd = [
                    'ffmpeg',
                    '-i', input_file,
                    '-c:v', 'libx265',
                    '-crf', '23',  # Adjust for quality as needed
                    '-c:a', 'aac',
                    '-b:a', '128k',
                    '-ac', '2',  # 2 channels for stereo
                    '-map', '0',  # Map all streams (video, audio, subtitles) from input to output
                    '-strict', 'experimental',
                    output_file
                ]

                # Run the command
                subprocess.run(cmd)
                print(f"Conversion completed for {input_file} to {output_file}")

        except Exception as e:
            print(f"Error processing file {file}. Error: {e}")

