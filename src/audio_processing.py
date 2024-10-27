# audio_processing.py
import os
from pydub import AudioSegment
from pydub.silence import detect_silence
from audio_segment_chunk import AudioSegmentChunk

def split_audio_in_chunks(audio_path, silence_duration=1500, buffer_duration=150):
    audio = AudioSegment.from_wav(audio_path)
    silence_threshold = audio.dBFS - 16
    silences = detect_silence(audio, min_silence_len=silence_duration, silence_thresh=silence_threshold)
    chunks = []
    start_time = 0

    for start, end in silences:
        # Aggiungi un buffer alla fine per includere le parole troncate
        end_with_buffer = min(end + buffer_duration, len(audio))

        chunk = AudioSegmentChunk(start_time, end_with_buffer, audio[start_time:end_with_buffer])
        chunks.append(chunk)
        chunk.export()  # Esporta utilizzando la logica di naming originale
        start_time = end
        print(chunk)

    # Aggiungi l'ultimo chunk se c'è del materiale rimanente
    if start_time < len(audio):
        chunk = AudioSegmentChunk(start_time, len(audio), audio[start_time:])
        chunks.append(chunk)
        chunk.export()  # Esporta anche l'ultimo chunk
        print("Adding last entry as ", chunk)

    return chunks

def remove_all_temp_files(chunks):
    for chunk in chunks:
        chunk.remove_temp_file()