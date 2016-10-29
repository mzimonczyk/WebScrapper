import logging
import json
import re
from DataParser import DataParser
from time import strptime


class WizzairParser(DataParser):
    def __init__(self, timestamp):
        columns = ['TIMESTAMP', 'DEPARTURE', 'DESTINATION', 'DEPARTURE_TIME', 'PRICE', 'CURRENCY']
        table_name = 'WIZZAIR'
        DataParser.__init__(self, timestamp, table_name, columns)

    def parse_data(self, content):
        data = json.loads(content)
        for day in data:
            self._parse_day(day)

    def _parse_day(self, data):
        date = data['CurrentDate']
        for flight in data['Flights']:
            minimum_price, currency = data['MinimumPrice'].split(' ')
            minimum_price = minimum_price.replace(u'\xa0', u'')
            departure = flight['DepartureStationName']
            destination = flight['ArrivalStationName']
            departure_time = strptime(date + ' ' + flight['STD'], "%Y-%m-%d %H:%M")
            self._data.add_row([
                    self._timestamp
                    , departure
                    , destination
                    , departure_time
                    , minimum_price
                    , currency
                    ])






