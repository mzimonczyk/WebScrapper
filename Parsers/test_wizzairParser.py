# -*- coding: utf-8 -*-

from unittest import TestCase
from Parsers.WizzairParser import WizzairParser
from time import strptime


class TestWizzairParser(TestCase):
    def test_parse_data(self):
        with open('Parsers\\test_wizzair.json') as f:
            content_with_five_records = f.read()

        parser = WizzairParser('some_date')

        parser.parse_data(content_with_five_records)
        data = parser.get_data()

        self.assertEqual(len(data.get_rows()), 30)
        self.assertEqual(data.get_rows()[0][1], u'Gdańsk')
        self.assertEqual(data.get_rows()[0][3], strptime("2016-06-28 19:20", "%Y-%m-%d %H:%M"))
        self.assertEqual(data.get_rows()[0][4], u'159,00')
        self.assertEqual(data.get_rows()[0][5], u'zł')
