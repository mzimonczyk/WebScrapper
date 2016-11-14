from unittest import TestCase
from Configuration.SourceDescription import SourceDescription
from Parsers.RyanairParser import RyanairParser
from time import strptime
import datetime


class TestRyanairParser(TestCase):
    def test_parse_data_correctly_parse_sample_data(self):
        with open(r'parsers\test_ryanair_content.json') as f:
            content = f.read()
        parser = RyanairParser('some_date')

        parser.parse_data(content)
        data = parser.get_data()

        self.assertEqual(len(data.get_rows()), 6)
        self.assertEqual(data.get_rows()[0][1], 'KTW')
        self.assertEqual(data.get_rows()[0][2], 'STN')
        self.assertEqual(data.get_rows()[0][3], strptime("2016-12-01 15:00:00", "%Y-%m-%d %H:%M:%S"))
        self.assertEqual(data.get_rows()[0][4], 104.25)
        self.assertEqual(data.get_rows()[0][5], 139)
        self.assertEqual(data.get_rows()[0][6], 'PLN')
        self.assertEqual(data.get_rows()[0][7], 5)

    def test_parse_data_correctly_parse_invalid_content(self):
        with open(r'parsers\test_ryanair_invalid_content.json') as f:
           content = f.read()
        parser = RyanairParser('some_date')
        parser.parse_data(content)
        data = parser.get_data()

        self.assertEqual(len(data.get_rows()), 0)

    def test_modify_source_desc_works(self):
        url =           'https://desktopapps.ryanair.com/pl-pl/availability?ADT=2&CHD=0&DateOut=2016-11-01&Destination=KTW&FlexDaysOut=6&INF=0&Origin=PLM&RoundTrip=false&TEEN=0'
        expected_url =  'https://desktopapps.ryanair.com/pl-pl/availability?ADT=2&CHD=0&DateOut=2016-11-08&Destination=KTW&FlexDaysOut=6&INF=0&Origin=PLM&RoundTrip=false&TEEN=0'
        source_desc = SourceDescription('GET', url)
        parser = RyanairParser('some_date')
        parser._first_date = datetime.datetime.strptime('2017-11-30T00:00:00.000', "%Y-%m-%dT%H:%M:%S.000")

        parser.modify_source_desc(source_desc)

        self.assertTrue(parser.has_more_data())
        self.assertEqual(source_desc.url, expected_url)

    def test_modify_source_desc_return_no_more_data_when_date_expires(self):
        url = 'https://desktopapps.ryanair.com/pl-pl/availability?ADT=2&CHD=0&DateOut=2016-11-01&Destination=KTW&FlexDaysOut=6&INF=0&Origin=PLM&RoundTrip=false&TEEN=0'
        source_desc = SourceDescription('GET', url)
        parser = RyanairParser('some_date')
        parser._first_date = datetime.datetime.strptime('2015-11-01T00:00:00.000', "%Y-%m-%dT%H:%M:%S.000")

        parser.modify_source_desc(source_desc)

        self.assertFalse(parser.has_more_data())
        self.assertEqual(source_desc.url, url)