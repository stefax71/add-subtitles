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
    def __init__(self, start: int, end: int, duration: int, translated_text:str = None):
        self.start = start
        self.end = end
        self.duration = duration
        self.original_text = None
        self.translated_text = translated_text
        self.audio_file = None

    def __str__(self):
        return f"Segment: {self.start} - {self.end} ({self.duration}) - recognized text {self.original_text}"

    def get_srt_timestamps(self):
        return self.translate_to_timestamp(self.start), self.translate_to_timestamp(self.end)

    def translate_to_timestamp(self, milliseconds: int) -> str:
        ore = milliseconds // (1000 * 60 * 60)
        minuti = (milliseconds // (1000 * 60)) % 60
        secondi = (milliseconds // 1000) % 60
        msec = milliseconds % 1000
        return f"{ore:02}:{minuti:02}:{secondi:02},{msec:03}"


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


    def merge_silences(self, silences: list[int], min_duration: int):
        """
        Merges consecutive silences if the gap between them is less than the specified minimum duration.

        Args:
            silences (list of list of int): A list of silences, where each silence is represented as a list [start, end].
            min_duration (int): The minimum duration (in milliseconds) between consecutive silences to consider them separate.

        Returns:
            list of list of int: A list of merged silences.
        """
        merged = []
        for silence in silences:
            if not merged:
                # If the merged list is empty, add the first silence
                merged.append(silence)
            else:
                prev_start, prev_end = merged[-1]
                curr_start, curr_end = silence
                # If the gap between the end of the previous silence and the start of the current silence is less than the minimum duration
                if curr_start - prev_end < min_duration:
                    # Merge the current silence with the previous one
                    merged[-1] = [prev_start, max(prev_end, curr_end)]
                else:
                    # Otherwise, add the current silence as a new entry
                    merged.append(silence)
        return merged

    def detect_segments(self):
        # Carica l'audio completo
        print("Detecting silences")
        audio = AudioSegment.from_file(self.audio_file, format="wav")

        silence_threshold = audio.dBFS - 16
        silences = detect_silence(audio, min_silence_len=600, silence_thresh=silence_threshold)

        segments = []
        silences = self.merge_silences(silences, 3000)

        previous_silence = None
        for silence in silences:
            if previous_silence is not None:
                duration = silence[0] - previous_silence
                print("Chunk da ", self.format_time(previous_silence), " a ", self.format_time(silence[0]),
                      " durata ms", duration)
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
