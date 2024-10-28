import json
import os

class AudioSegmentChunk:

    def __init__(self, start, end, wav, audio_file_name=""):
        self._start = start
        self._end = end
        self._wav = wav
        self._audio_file_name = audio_file_name
        self._text = ""

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        self._end = value

    @property
    def wav(self):
        return self._wav

    @wav.setter
    def wav(self, value):
        self._wav = value

    @property
    def audio_file_name(self):
        return self._audio_file_name

    @audio_file_name.setter
    def audio_file_name(self, value):
        self._audio_file_name = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    def duration(self):
        return self.end - self.start

    def get_time_in_seconds(self):
        start_seconds = self.start / 1000
        end_seconds = self.end / 1000
        return (start_seconds, end_seconds)

    def get_start_time_in_seconds(self):
        return self.get_srt_timestamp(self.start)

    def get_srt_timestamp(self, time_ms):
        hours = time_ms // 3600000
        minutes = (time_ms % 3600000) // 60000
        seconds = (time_ms % 60000) // 1000
        milliseconds = time_ms % 1000
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{int(milliseconds):03}"

    def get_srt_timestamps(self):
        start_srt = self.get_srt_timestamp(self.start)
        end_srt = self.get_srt_timestamp(self.end)
        return (start_srt, end_srt)

    def add_text(self, text):
        self.text = text

    def export(self):
        temp_path = "/app/videos/tmp/"
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
            print(f"Directory {temp_path} creata con successo.")

        self.audio_file_name = temp_path + "chunk_" + str(self.start) + "_" + str(self.end) + ".wav"
        audio = self.wav.set_frame_rate(16000).set_channels(1)
        audio.export(self.audio_file_name, format="wav")
        return self.audio_file_name

    def remove_temp_file(self):
        os.remove(self.audio_file_name)

    def __str__(self):
        start_srt, end_srt = self.get_srt_timestamps()
        return f"Segmento {start_srt} --> {end_srt} file: {self.audio_file_name}"