import openai
from openai import OpenAI

from silence_detector import Segment


def recognize_from_audio(seg: Segment):
    print ("Recognizing audio from segment ", seg)
    client = OpenAI()

    audio_file= open(seg.audio_file, "rb")
    translation = client.audio.transcriptions.create(
        prompt="Considera un contesto assicurativo vita in cui si parla si switch, swap, finanziario, tassi di interesse.",
        model="whisper-1",
        file=audio_file,
        temperature=0.2
    )
    print("DEBUG -> ", translation.text)
    seg.original_text = translation.text

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "Sei un esperto traduttore specializzato in ambito assicurativo vita che traduce SOLO in inglese. Si parla di swap, quittance, maturity, surrender e switch."
                    "Traduci il testo seguente in inglese, e rispondi esclusivamente con il testo tradotto. "
                    "Presta attenzione a non usare altre lingue oltre l'inglese"
                    "Non utilizzare punti alla fine delle frasi."
                    "Presta attenzione alla terminologia che sia coerente con l'ambito assicurativo vita e cerca di mantenere il significato originale del testo."
                )
            },
            {
                "role": "user",
                "content": f"{seg.original_text}",
            }
        ],
        model="gpt-4o",
    )
    seg.translated_text = chat_completion.choices[0].message.content
    return seg