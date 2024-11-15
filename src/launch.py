import os

from dotenv import load_dotenv

from add_subtitles import AddSubtitles
from config import base_path

print("Searching for videos: ", base_path)

add_subtitles = AddSubtitles()
found_videos = add_subtitles.run()

# for video in found_videos:
#     add_subtitles.process_file(video)