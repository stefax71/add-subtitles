import re
import subprocess

from pydub import AudioSegment
from pydub.silence import detect_silence

class AudioSilence:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
        self.duration = end - start

    def __str__(self):
        return f"Silence: Start at {self.start}, ends at {self.end}, duration {self.duration}"


class Segment:
    def __init__(self, start: float, end: float, duration: float):
        self.start = start
        self.end = end
        self.duration = duration
        self.text = None
        self.audio_file = None

    def __str__(self):
        return f"Segment: {self.start} - {self.end} ({self.duration}) - recognized text {self.text}"


class SegmentsDetector:
    def __init__(self, audio_file: str, temp_dir: str):
        super().__init__()
        self.audio_file = audio_file
        self.temp_dir = temp_dir

    def format_time(self, milliseconds: float) -> str:
        seconds = milliseconds // 1000
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        remaining_seconds = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"

    def detect_segments(self):
        # Carica l'audio completo
        print("Detecting silences")
        audio = AudioSegment.from_file(self.audio_file, format="wav")

        silence_threshold = audio.dBFS - 16
        silences = detect_silence(audio, min_silence_len=300, silence_thresh=silence_threshold)

        segments = []
        previous_silence = None
        for silence in silences:
            silence_object = AudioSilence(silence[0], silence[1])
            if previous_silence is not None:
                duration = silence[0] - previous_silence
                print("Chunk da ", self.format_time(previous_silence), " a ", self.format_time(silence[0]), " durata ms", duration)
                segment = Segment(start=previous_silence, end=silence[0], duration=duration)
                segments.append(segment)
            previous_silence = silence[1]

        return segments


        # subprocess.run(
        #     ['ffmpeg', '-i', self.audio_file, '-af', 'silencedetect=noise=-30dB:d=0.5', '-f', 'null', '-'],
        #     stderr=open(silence_file, 'w')
        # )

        # # Leggi i timestamp dai log
        # segments = []
        #
        # silence_end_pattern = r"silence_end:\s*([\d.]+)\s*\|\s*silence_duration:\s*([\d.]+)"
        # silence_start_pattern = r"silence_start:\s*([\d.]+)"
        #
        # with open(self.temp_dir + "/silence_log.txt", "r") as log_file:
        #     for line in log_file:
        #         if "silence_start" in line:
        #             match = re.search(silence_start_pattern, line)
        #             start = float(match.group(1))
        #         elif "silence_end" in line:
        #             match = re.search(silence_end_pattern, line)
        #             end = float(match.group(1))
        #             duration = float(match.group(2))
        #             segments.append(Segment(start, end, duration))
        #
        # # Suddividi l'audio usando i timestamp
        # # for i, (start, end) in enumerate(segments):
        # #     segment = audio[start * 1000:end * 1000]  # Conversione in millisecondi
        # #     segment.export(f"segment_{i + 1:03d}.wav", format="wav")
        # print("Segmenti creati con successo!")
        # for segment in segments:
        #     print(segment)
