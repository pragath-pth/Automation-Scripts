import os
import shutil
from mutagen.flac import FLAC
from mutagen.wave import WAVE
from mutagen.id3 import ID3
from mutagen.mp4 import MP4
import re

# Define the directory containing your FLAC, WAV, and M4A files
source_directory = r'E:\Malayalam'
# Define the directory where you want to organize the albums
destination_directory = r'E:\Malayalam'

# Ensure the destination directory exists
os.makedirs(destination_directory, exist_ok=True)

# Function to sanitize folder names
def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', ' ', name)

# Iterate over each file in the source directory
for filename in os.listdir(source_directory):
    if filename.endswith(('.flac', '.wav', '.m4a')):
        # Construct the full path to the file
        file_path = os.path.join(source_directory, filename)
        
        # Initialize album, year, and format variables
        album = 'Unknown Album'
        year = 'YYYY'
        file_format = filename.split('.')[-1].upper()

        # Extract album tag and year from FLAC, WAV, or M4A file
        if filename.endswith('.flac'):
            try:
                audio = FLAC(file_path)
                album = audio.get('album', [album])[0]
                year = audio.get('date', [year])[0]
            except Exception as e:
                print(f"Error reading {filename}: {e}")
        elif filename.endswith('.wav'):
            try:
                audio = WAVE(file_path)
                if hasattr(audio, 'tags') and audio.tags:
                    if 'TALB' in audio.tags:
                        album = audio.tags['TALB'].text[0]
                    if 'TYER' in audio.tags:
                        year = audio.tags['TYER'].text[0]
                else:
                    # Attempt to read ID3 tags if available
                    try:
                        id3 = ID3(file_path)
                        album = id3.get('TALB', [album])[0]
                        year = id3.get('TYER', [year])[0]
                    except Exception as e:
                        print(f"ID3 tag reading error for {filename}: {e}")
            except Exception as e:
                print(f"Error reading {filename}: {e}")
        elif filename.endswith('.m4a'):
            try:
                audio = MP4(file_path)
                album = audio.tags.get('\xa9alb', [album])[0]
                year = audio.tags.get('\xa9day', [year])[0][:4]  # Extract only the year part
            except Exception as e:
                print(f"Error reading {filename}: {e}")

        # Sanitize the album and year
        album_sanitized = sanitize_filename(album)
        year_sanitized = sanitize_filename(year)
        file_format_sanitized = sanitize_filename(file_format)

        # Create the folder name in the format "Album Name - Year - File Format"
        folder_name = f"{album_sanitized} - {year_sanitized} - {file_format_sanitized}"
        album_directory = os.path.join(destination_directory, folder_name)
        os.makedirs(album_directory, exist_ok=True)
        
        # Move the file to the album directory
        destination_path = os.path.join(album_directory, filename)
        shutil.move(file_path, destination_path)
        
        print(f'Moved {filename} to {album_directory}')

print('Done organizing audio files.')
