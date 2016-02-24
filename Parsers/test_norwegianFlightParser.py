# -*- coding: utf-8 -*-

from unittest import TestCase
from Parsers.NorwegianFlightParser import NorwegianFlightParser


class TestNorwegianFlightParser(TestCase):
    def test_parse_data_correctly_parse_sample_data(self):
        with open('Parsers\\test_norwegian_GDN_NRV.html') as f:
            content_with_3_flights = f.read()

        parser = NorwegianFlightParser('some_date')

        parser.parse_data(content_with_3_flights)
        data = parser.get_data()

        self.assertEqual(len(data.get_rows()), 3)
        self.assertEqual(data.get_rows()[0][1], u'Gdansk')
        self.assertEqual(data.get_rows()[0][2], u'13:55')
        self.assertEqual(data.get_rows()[0][3], u'Harstad/Narvik')
        self.assertEqual(data.get_rows()[0][4], u'19:35')
        self.assertEqual(data.get_rows()[0][5], u'706')
        self.assertEqual(data.get_rows()[0][6], u'804')
        self.assertEqual(data.get_rows()[0][7], u'1 693')
#   wylot   przylot szczegóły   lowafare    lowfare+    flex info