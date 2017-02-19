from unittest import TestCase
from Parsers.AzairParser import AzairParser
from time import strptime


class TestAzairParser(TestCase):
    def test_parse_data(self):
        with open('Parsers\\test_azair.eu_content.html') as f:
            content = f.read()
        parser = AzairParser('some_date')

        parser.parse_data(content)
        data = parser.get_data()

        self.assertEqual(63, len(data.get_rows()))

    def test_parse_data_successfully_parse_content(self):
        with open('Parsers\\test_azair.eu_one_result.html') as f:
            content = f.read()
        parser = AzairParser('some_date')

        parser.parse_data(content)
        data = parser.get_data()

        self.assertEqual(1, len(data.get_rows()))
        row = data.get_rows()[0]

        self.assertEqual('Warsaw WAW', row[1]) # DEPARTURE
        self.assertEqual(strptime('28/04/17 16:20', "%d/%m/%y %H:%M"), row[2] ) # THERE_DEPARTURE_TIME
        self.assertEqual(strptime('28/04/17 19:35', "%d/%m/%y %H:%M"), row[3] ) # THERE_ARRIVAL_TIME
        self.assertEqual('Wizz Air', row[4] ) # THERE_AIRLINE
        self.assertEqual('478', row[5] ) # THERE_PRICE
        self.assertEqual('Santander SDR', row[6] ) # DESTINATION
        self.assertEqual(strptime('08/05/17 20:20', "%d/%m/%y %H:%M"), row[7] ) # BACK_DEPARTURE_TIME
        self.assertEqual(strptime('08/05/17 23:30', "%d/%m/%y %H:%M"), row[8] ) # BACK_ARRIVAL_TIME
        self.assertEqual('Wizz Air', row[9] ) # BACK_AIRLINE
        self.assertEqual('303', row[10] ) # BACK_PRICE
        self.assertEqual('782', row[11] ) # PRICE
