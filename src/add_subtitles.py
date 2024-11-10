# Tool per aggiungere sottotitoli ad un video
import glob
import os
import subprocess

from audio_processing import split_audio_in_chunks, remove_all_temp_files
from openai_config_reader import openai_read_configuration
from openai_refiner import  OpenAIRefiner
from config import base_path
from transcriber import recognize_speech
from srt_generator import save_entries_to_srt

class AddSubtitles:

    def find_files_to_process(self):
        print (base_path)
        pattern = os.path.join("/app/videos/", '**', '*.mp4')
        return glob.glob(pattern, recursive=True)

    def process_file(self, video_path: str):
        # Estrai il nome del file senza l'estensione
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        # Crea una directory con questo nome

        output_dir = os.path.join("/app/videos", base_name)
        print("Processing video: ", video_path)
        os.makedirs(output_dir, exist_ok=True)

        # Percorso del file audio temporaneo
        audio_path = os.path.join(output_dir, "audio_temp_16k_mono.wav")

        # Estrai e converte l'audio a 16kHz mono
        command = [
            "ffmpeg", "-i", video_path, "-ac", "1", "-ar", "16000", "-sample_fmt", "s16", audio_path
        ]
        subprocess.run(command, check=True)
        chunks = split_audio_in_chunks(audio_path)
        entries = recognize_speech(chunks)
        save_entries_to_srt(entries, filename= output_dir + "/output_original_unprocessed.srt")

