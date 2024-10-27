# srt_generation.py
def generate_srt_entry(chunk, text, index):
    start_srt, end_srt = chunk.get_srt_timestamps()
    srt_entry = f"{index}\n{start_srt} --> {end_srt}\n{text}\n"
    return srt_entry

def save_entries_to_srt(entries, filename="output.srt"):
    with open(filename, "w", encoding="utf-8") as srt_file:
        for entry in entries:
            srt_file.write(entry + "\n")