# srt_generation.py
import re

import config
from silence_detector import Segment


class SubtitleElement:
    def __init__(self, index, start, end, text):
        self.index = index
        self.start = start
        self.end = end
        self.text = text


    def __str__(self):
        return f"{self.index}\n{self.start} --> {self.end}\n{self.text}\n"


class SrtGenerator:
    def __init__(self, chunks: list[Segment]):
        self.chunks = chunks
        self.entries = []


    def generate_srt(self, max_duration=10):
        entries = self.generate_srt_entry()
        self.entries = self.split_long_lines_into_chunks(entries, max_duration)
        return self.entries


    def write(self, filename:str="output.srt"):
        with open(filename, "w", encoding="utf-8") as srt_file:
                for entry in self.entries:
                    srt_file.write(str(entry) + "\n")


    def generate_srt_entry(self):
        entries = []
        for i, chunk in enumerate(self.chunks):
            start_srt, end_srt = chunk.get_srt_timestamps()
            entry = SubtitleElement(i + 1, start_srt, end_srt, chunk.translated_text)
            entries.append(entry)
        return entries


    # Refined function to split subtitles and ensure proper text segmentation
    def split_long_lines_into_chunks(self, subs, max_duration=10):
        new_subs = []
        for sub in subs:
            start_seconds = self.time_to_milliseconds(sub.start)
            end_seconds = self.time_to_milliseconds(sub.end)
            duration = end_seconds - start_seconds
            print("-" * 20)
            print("Original entry is ", str(sub))
            print("Processing entry #", sub.index, " starting at ", start_seconds, " end at " , end_seconds,   " with duration ", duration, " seconds")

            if duration > (max_duration * 1000):
                print("Splitting entry")
                # Spezza il file tenendo conto della lunghezza in secondi e del numero di parole
                # così da calcolare in modo ragionevolmente corretto dove iniziano i sotto-chunks

                words = sub.text.split()
                avg_words_per_chunk = len(words) / int( ((duration // max_duration) // 1000) + 1)

                chunk_start = start_seconds
                for i in range(0, len(words), int(avg_words_per_chunk)):
                    chunk_end = min(chunk_start + (max_duration * 1000), end_seconds)
                    chunk_text = ' '.join(words[i:i + int(avg_words_per_chunk)])

                    sub = SubtitleElement(index = len(new_subs) + 1, start=self.seconds_to_time(chunk_start), end=self.seconds_to_time(chunk_end), text=chunk_text)
                    new_subs.append(sub)

                    chunk_start = chunk_end
            else:
                sub = SubtitleElement(index=len(new_subs) + 1, start=sub.start, end=sub.end, text=sub.text)
                new_subs.append(sub)
        return new_subs


    def time_to_milliseconds(self, timestamp):
        hours, minutes, seconds, msec = map(float, re.split('[:,.]', timestamp))
        return (hours * 3600 + minutes * 60 + seconds) * 1000 + msec


    def seconds_to_time(self, seconds):
        ms = seconds / 1000
        hours = int(ms // 3600)
        minutes = int((ms % 3600) // 60)
        secs = int(ms % 60)
        millis = round((ms - int(ms)) * 1000)
        return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"
