# speech_recognition.py
import wave
from vosk import Model, KaldiRecognizer

from srt_generator import generate_srt_entry


def recognize_speech(chunks, model_path):
    model = Model(model_path)
    rec = KaldiRecognizer(model, 16000)
    entries = []
    for chunk in chunks:
        print("************************************", flush=True)
        print("Processing chunk: ", chunk, flush=True)
        with wave.open(chunk.audio_file_name, "rb") as wf:
            while True:
                data = wf.readframes(1000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    res = rec.Result()
                    print("Text found: ", res, flush=True)
                    chunk.add_text(res)

    for i, chunk in enumerate(chunks):
        entries.append(generate_srt_entry(chunk, chunk.text, i))
    return entries