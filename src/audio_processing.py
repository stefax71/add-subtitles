# audio_processing.py
import os
import re
import subprocess

from pydub import AudioSegment
from pydub.silence import detect_silence
from audio_segment_chunk import AudioSegmentChunk


def split_audio_by_silence(input_file, min_duration=10, noise_level='-30dB', silence_duration=0.5,
                           output_dir='output_chunks'):
    """
    Divide un file audio in segmenti basati sui silenzi, assicurandosi che ogni segmento abbia una durata minima.

    Args:
        input_file (str): Percorso del file audio di input.
        min_duration (int): Durata minima in secondi per ogni segmento.
        noise_level (str): Soglia del volume per rilevare il silenzio (es. '-30dB').
        silence_duration (float): Durata minima del silenzio in secondi per essere rilevato.
        output_dir (str): Directory di output per i segmenti.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Comando per rilevare i silenzi
    cmd = [
        'ffmpeg', '-i', input_file, '-af',
        f'silencedetect=noise={noise_level}:d={silence_duration}', '-f', 'null', '-'
    ]

    # Esegui il comando e cattura l'output
    result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
    output = result.stderr

    # Estrai i timestamp di inizio e fine del silenzio
    silence_starts = []
    for line in output.splitlines():
        start_match = re.search(r'silence_start: (\d+\.\d+)', line)
        end_match = re.search(r'silence_end: (\d+\.\d+)', line)

        if start_match:
            silence_starts.append(float(start_match.group(1)))
        elif end_match and silence_starts:
            silence_end = float(end_match.group(1))
            silence_starts[-1] = (silence_starts[-1], silence_end)

    # Genera i segmenti basati sulla durata minima
    start_time = 0
    segment_num = 1

    for silence_start, silence_end in silence_starts:
        # Calcola la durata del segmento
        segment_duration = silence_start - start_time

        if segment_duration >= min_duration:
            output_file = os.path.join(output_dir, f'chunk_{segment_num}.wav')
            # Crea il segmento con ffmpeg
            subprocess.run([
                'ffmpeg', '-i', input_file, '-ss', str(start_time), '-to', str(silence_start),
                '-c', 'copy', output_file
            ])

            print(f"Creato segmento: {output_file}")
            segment_num += 1
            start_time = silence_end

    # Crea l'ultimo segmento se rimasto
    if start_time < float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                                          'format=duration', '-of',
                                          'default=noprint_wrappers=1:nokey=1', input_file],
                                         stdout=subprocess.PIPE,
                                         text=True).stdout.strip()):
        output_file = os.path.join(output_dir, f'chunk_{segment_num}.wav')
        subprocess.run([
            'ffmpeg', '-i', input_file, '-ss', str(start_time), '-c', 'copy', output_file
        ])
        print(f"Creato ultimo segmento: {output_file}")


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