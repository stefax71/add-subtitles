from openai import OpenAI


def recognize_from_audio(audio_file):
    client = OpenAI()

    audio_file= open(audio_file, "rb")
    translation = client.audio.translations.create(
      model="whisper-1",
      file=audio_file
    )
    return translation.text