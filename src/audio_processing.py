# audio_processing.py
import os
from pydub import AudioSegment
from pydub.silence import detect_silence
from audio_segment_chunk import AudioSegmentChunk

def split_audio_in_chunks(audio_path, silence_duration=1500, buffer_duration=150, max_chunk_duration=8000):
    audio = AudioSegment.from_wav(audio_path)
    silence_threshold = audio.dBFS - 16
    silences = detect_silence(audio, min_silence_len=silence_duration, silence_thresh=silence_threshold)
    chunks = []
    start_time = 0

    for start, end in silences:
        end_with_buffer = min(end + buffer_duration, len(audio))

        while start_time < end_with_buffer:
            chunk_end_time = min(start_time + max_chunk_duration, end_with_buffer)
            chunk = AudioSegmentChunk(start_time, chunk_end_time, audio[start_time:chunk_end_time])
            chunks.append(chunk)
            chunk.export()
            print(chunk)

            start_time = chunk_end_time

        start_time = end_with_buffer

    while start_time < len(audio):
        chunk_end_time = min(start_time + max_chunk_duration, len(audio))
        chunk = AudioSegmentChunk(start_time, chunk_end_time, audio[start_time:chunk_end_time])
        chunks.append(chunk)
        chunk.export()
        print("(last)", chunk)
        start_time = chunk_end_time

    return chunks

def remove_all_temp_files(chunks):
    for chunk in chunks:
        chunk.remove_temp_file()