from openai import OpenAI

from silence_detector import Segment


def recognize_from_audio(seg: Segment):
    client = OpenAI()

    audio_file= open(seg.audio_file, "rb")
    translation = client.audio.translations.create(
      model="whisper-1",
      file=audio_file
    )
    return translation.text