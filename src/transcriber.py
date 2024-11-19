# speech_recognition.py
from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor

from whisperer_recognize import recognize_from_audio


def process_chunk(chunk):
    try:
        print("Processing chunk: ", chunk.audio_file_name)
        text = recognize_from_audio(chunk.audio_file_name)
        chunk.add_text(text)
    except Exception as e:
        print("Error processing chunk ", chunk.audio_file_name ,": ", e)


def recognize_speech(chunks):
    entries = []
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_chunk, chunk): chunk for chunk in chunks}
        for future in as_completed(futures):
            future.result()

    chunks.sort(key=lambda x: x.start)

    entries = [generate_srt_entry(chunk, chunk.original_text, i) for i, chunk in enumerate(chunks)]
    return entries