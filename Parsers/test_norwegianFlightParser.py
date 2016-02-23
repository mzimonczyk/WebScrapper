# -*- coding: utf-8 -*-

from unittest import TestCase
from Parsers.NorwegianFlightParser import NorwegianFlightParser


class TestNorwegianFlightParser(TestCase):
    def test_parse_data_correctly_parse_sample_data(self):
        with open('test_norwegian_GDN_NRV.html') as f:
            content_with_3_flights = f.read()

        parser = NorwegianFlightParser('some_date')

        parser.parse_data(content_with_3_flights)
        data = parser.get_data()

        self.assertEqual(len(data.get_rows()), 3)
#   wylot   przylot szczegóły   lowafare    lowfare+    flex info