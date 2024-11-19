# tests/test_srt_generator.py
import unittest
from src.srt_generator import SrtGenerator, SubtitleElement
from src.silence_detector import Segment

class TestSrtGenerator(unittest.TestCase):
    def setUp(self):
        # Create some example segments
        self.segments = [
            Segment(start=9176, end=43088, duration = 33913,  translated_text="direttamente funzionali previsti. In realtà avevamo previsto un incontro anche il 22 e l'idea era quella di approfondire il tema dell'usurpo che era emerso la scorsa volta con Gemma, quando abbiamo visto i processi massivi più legati alla parte finanziaria. Mentre oggi il focus sarà sui processi massivi che non sono prettamente legati alla parte finanziaria, in particolare le riserve e la rivalutazione. Ciao Gemma!"),
        ]
        self.generator = SrtGenerator(self.segments)

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