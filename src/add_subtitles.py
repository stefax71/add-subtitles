# Tool per aggiungere sottotitoli ad un video
import glob
import os
import subprocess

import config
from audio_processing import split_audio_in_chunks, remove_all_temp_files
from openai_config_reader import openai_read_configuration
from openai_refiner import  OpenAIRefiner
from transcriber import recognize_speech
from video_processor import VideoProcessor


class AddSubtitles:
    def __init__(self):
        super().__init__()
        if (config.base_path == None):
            raise RuntimeError("Base path not set")


    def run(self):
        videos = self.find_files_to_process()
        for video in videos:
            video_processor = VideoProcessor(video)
            video_processor.process_file()

    def find_files_to_process(self):
        print("Searching in ", config.base_path)
        pattern = os.path.join(config.base_path, '**', '*.mp4')
        return glob.glob(pattern, recursive=True)

