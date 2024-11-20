import os
import pickle
import subprocess
import tempfile

from pydub import AudioSegment
from pydub.silence import detect_silence

import config
from silence_detector import SegmentsDetector
from srt_generator import SrtGenerator
from whisperer_recognize import recognize_from_audio


class VideoProcessor:

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path

    def process_file(self):
        print("Processing file ", self.file_path)
        # Estrai il nome del file senza l'estensione
        base_name = os.path.splitext(os.path.basename(self.file_path))[0]

        self.temp_dir = tempfile.gettempdir() + "/" + base_name + "_tmp"
        print("Creating temporary directory ", self.temp_dir)
        os.makedirs(self.temp_dir, exist_ok=True)
        audio_path = self.extract_audio()

        segments_detector = SegmentsDetector(audio_path, self.temp_dir)
        segments = segments_detector.detect_segments()


        audio = AudioSegment.from_file(audio_path, format="wav")

        for i, segment in enumerate(segments):
            delta = 0
            delta_end = 0

            if i > 0:
                delta = (segment.start - segments[i - 1].end) // 2
            if i < len(segments) - 1:
                delta_end = (segments[i + 1].start - segment.end) // 2

            start = segment.start - delta
            end = segment.end + delta_end
            chunk = audio[start:end]
            wave_file = self.temp_dir + "/chunk_" + str(segment.start) + ".wav"
            chunk.export(wave_file, format="wav")
            segment.audio_file = wave_file
            recognize_from_audio(segment)


        with open(self.temp_dir + "/segments.dat", "ab") as dest_file:
            pickle.dump(segments, dest_file)

        exit(0)
        srt_generator = SrtGenerator(segments)
        srt_generator.generate_srt()
        srt_generator.write(config.base_path + "/english.srt")


    def extract_audio(self):
        print("Extracting audio from video using ffmpeg")
        # Percorso del file audio temporaneo
        audio_path = os.path.join(self.temp_dir, "audio_temp_16k_mono.wav")
        # Estrai e converte l'audio a 16kHz mono
        command = [
            "ffmpeg", "-i", self.file_path, "-ac", "1", "-ar", "16000", "-sample_fmt", "s16", "-filter:a", "volume=5dB", audio_path
        ]
        subprocess.run(command, check=True)
        return audio_path
