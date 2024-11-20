# tests/test_srt_generator.py
import pickle
import unittest
from src.srt_generator import SrtGenerator, SubtitleElement
from src.silence_detector import Segment

class TestSrtGenerator(unittest.TestCase):
    def setUp(self):
        # Create some example segments
        self.segments = [
            Segment(start=285603, end=305735, duration = 20132,  translated_text="based also on the individual and collective portfolio, the calculation can be limited to the ministerial branch. It is then necessary to indicate the reference date for the calculation of the reserve, usually the last day of the month"),
        ]
        self.generator = SrtGenerator(self.segments)


    def test_load_elements(self):
        with open("/tmp/sample_tmp/segments.dat", 'rb') as file:
            data = pickle.load(file)
        srt_generator = SrtGenerator(data)
        entries = srt_generator.generate_srt()
        print(data)

    def test_generate_srt(self):
        expected_output = [
            SubtitleElement(1, "00:00:09,176", "00:00:19,176", "direttamente funzionali previsti. In realtà avevamo previsto un incontro anche il 22 e l'idea era quella"),
            SubtitleElement(2, "00:00:19,176", "00:00:29,176", "di approfondire il tema dell'usurpo che era emerso la scorsa volta con Gemma, quando abbiamo visto"),
            SubtitleElement(3, "00:00:29,176", "00:00:39,176", "i processi massivi più legati alla parte finanziaria. Mentre oggi il focus sarà sui processi massivi"),
            SubtitleElement(4, "00:00:39,176", "00:00:43,088", "che non sono prettamente legati alla parte finanziaria, in particolare le riserve e la rivalutazione. Ciao"),
            SubtitleElement(5, "00:00:43,088", "00:00:43,088", "Gemma!")
        ]

        result = self.generator.generate_srt()
        self.generator.write("output.srt")

        self.assertEqual(len(result), len(expected_output))
        for res, exp in zip(result, expected_output):
            self.assertEqual(res.index, exp.index)
            self.assertEqual(res.start, exp.start)
            self.assertEqual(res.end, exp.end)
            self.assertEqual(res.text, exp.text)

if __name__ == '__main__':
    unittest.main()