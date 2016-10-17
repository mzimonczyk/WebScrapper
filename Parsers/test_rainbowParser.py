from unittest import TestCase
from Parsers.RainbowParser import RainbowParser

class TestRainbowParser(TestCase):
    def test_parse_data_correctly_parse_sample_data(self):
        with open('test_rainbow_content.html') as f:
            content = f.read()
        parser = RainbowParser('some_date')

        parser.parse_data(content)
        data = parser.get_data()
        print data
