from unittest import TestCase
from Parsers.RyanairParser import RyanairParser
from time import strptime


class TestRyanairParser(TestCase):
    def test_parse_data_correctly_parse_sample_data(self):
        with open('parsers\\test_ryanair_content.json') as f:
            content = f.read()
        parser = RyanairParser('some_date')

        parser.parse_data(content)
        data = parser.get_data()

        # self.assertEqual(len(data.get_rows()), 26)
        # self.assertEqual(data.get_rows()[0][1], 'Katowice')
        # self.assertEqual(data.get_rows()[0][2], 'Teneryfa')
        # self.assertEqual(data.get_rows()[0][3], strptime("2017-04-30", "%Y-%m-%d"))
        # self.assertEqual(data.get_rows()[0][4], 1541)
        # self.assertEqual(data.get_rows()[0][5], 103787)
