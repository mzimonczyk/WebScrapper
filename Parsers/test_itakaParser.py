# -*- coding: utf-8 -*-

from datetime import datetime
from time import strptime
from unittest import TestCase

from Parsers.ItakaParser import ItakaParser


class TestItakaParser(TestCase):
    def test_get_data_returns_some_data_after_calling_parse_data_on_content(self):
        with open('Parsers\\test_itaka.pl_content.json') as f:
            content_with_five_records = f.read()

        parser = ItakaParser('some_date')

        parser.parse_data(content_with_five_records)
        data = parser.get_data()

        self.assertEqual(len(data.get_rows()), 5)

    def test_has_more_data_returns_true_after_calling_parse_data_on_content_with_json_param_available_more_offers_set(
            self):
        json_string = '{"offers":"", "available_more_offers":true}'
        parser = ItakaParser('some_date')

        parser.parse_data(json_string)

        self.assertTrue(parser.has_more_data())
        pass

    def test_has_more_data_returns_false_after_calling_parse_data_on_content_with_json_param_available_more_offers_set(
            self):
        json_string = '{"offers":"", "available_more_offers":false}'
        parser = ItakaParser('some_date')

        parser.parse_data(json_string)

        self.assertFalse(parser.has_more_data())
        pass

    def test_parse_flight_description(self):
        # description = 'Warszawa (Polska) Barcelona (Hiszpania) Bilet tam i z powrotem Wylot 9 Styczen 05:00 (Sob) Warszawa, Okecie 08:10 (Sob) Barcelona, Barcelona Powrót 16 Styczen 09:00 (Sob) Barcelona, Barcelona 12:00 (Sob) Warszawa, Okecie W cenie: Bagaz Oplaty lotniskowe Rezerwuj 391pln '
        description = 'Katowice (Polska) Marsa Alam (Egipt) Bilet tam i z powrotem Wylot 27 Luty 09:00 (Sob) ' \
                      'Katowice, Pyrzowice 14:25 (Sob) Marsa Alam, Marsa Alam Intl Powrot 5 Marzec 15:15 (Sob) ' \
                      'Marsa Alam, Marsa Alam Intl 18:45 (Sob) Katowice, Pyrzowice W cenie: ' \
                      'Bagaz Oplaty lotniskowe Rezerwuj 1 346pln'
        parser = ItakaParser('some_date')

        parser.parse_flight_description(description)

        self.assertEqual(len(parser.get_data().get_rows()), 1)

    def test_parse_data_two_times_removes_old_data(self):
        with open('Parsers\\test_itaka.pl_content.json') as f:
            content_with_five_records = f.read()
        parser = ItakaParser('some_date')

        parser.parse_data(content_with_five_records)
        parser.parse_data(content_with_five_records)

        data = parser.get_data()

        self.assertEqual(len(parser.get_data().get_rows()), 5)

    def test_parse_flight_description_with_polish_characters(self):
        # description = 'Warszawa (Polska) Barcelona (Hiszpania) Bilet tam i z powrotem Wylot 9 Styczen 05:00 (Sob) Warszawa, Okecie 08:10 (Sob) Barcelona, Barcelona Powrót 16 Styczen 09:00 (Sob) Barcelona, Barcelona 12:00 (Sob) Warszawa, Okecie W cenie: Bagaz Oplaty lotniskowe Rezerwuj 391pln '
        description = u"Katowice (Polska) Marsa Alam (Egipt) Bilet tam i z powrotem Wylot 27 Luty 09:00 (Sob) " \
                      u"Katowice, Pyrzowice 14:25 (Sob) Marsa Alam, Marsa Alam Intl Powrót 5 Marzec 15:15 (Sob) " \
                      u"Marsa Alam, Marsa Alam Intl 18:45 (Sob) Katowice, Pyrzowice W cenie: " \
                      u"Bagaż Opłaty lotniskowe Rezerwuj 1 346pln"
        parser = ItakaParser('some_date')

        parser.parse_flight_description(description)

        self.assertEqual(1, len(parser.get_data().get_rows()))

    def test_format_date_correctly_formats_date(self):
        parser = ItakaParser('some_date')

        date = parser.format_date('9 Luty 12:30')

        self.assertEqual(strptime(str(datetime.now().year) + '-02-09 12:30:00', "%Y-%m-%d %H:%M:%S"), date)

    def test_format_date_correctly_formats_date_with_polish_chars(self):
        parser = ItakaParser('some_date')

        date = parser.format_date(u'9 Styczeń 12:30')

        self.assertEqual(strptime(str(datetime.now().year) + '-01-09 12:30:00', "%Y-%m-%d %H:%M:%S"), date)
