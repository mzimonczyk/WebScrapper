# -*- coding: utf-8 -*-

import logging
import json
import re
from DataParser import DataParser
from time import strptime


class RainbowParser(DataParser):
    def __init__(self, timestamp):
        columns = ['TIMESTAMP', 'DEPARTURE', 'DESTINATION', 'DEPARTURE_DATE', 'PRICE', 'R_ID']
        table_name = 'RAINBOW'
        DataParser.__init__(self, timestamp, table_name, columns)

    _destination_city = ''
    _source_city = ''

    def parse_data(self, content):
        flight_descriptions = self._get_flight_content(content)
        for description in flight_descriptions:
            self._parse_flights_description(description)

    def _get_flight_content(self, content):
        flight_content = []
        for line in content.split('\n'):
            self._find_source_city(line)
            self._find_destination_city(line)
            data = self._find_data(line)
            if data is not None:
                flight_content.append(data)
        return flight_content

    def _find_source_city(self, line):
        pattern ='<span class="kierunek">Wylot z:&nbsp;</span><span class="miasto">'
        if pattern in line:
            self._source_city = line.replace(pattern, '').replace('</span></h2>', '').strip()

    def _find_destination_city(self, line):
        pattern ='<span class="kierunek">Powr&#243;t z:&nbsp;</span><span class="miasto">'
        if pattern in line:
            self._destination_city = line.replace(pattern, '').replace('</span></h2>', '').strip()

    def _find_data(self, line):
        pattern ='dostepneLoty: '
        if pattern in line:
            return line.replace(pattern, '').strip().strip('\'')
        return None

    def _parse_flights_description(self, description):
        flights = json.loads(description)
        for flight in flights:
            self._parse_flight(flight)

    def _parse_flight(self, flight):
        date = self._format_date(flight['start'])
        price = int(flight['title'].replace(u'\xa0', ''))
        id = int(flight['id'])
        self._data.add_row([
            self._timestamp
            , self._source_city
            , self._destination_city
            , date
            , price
            , id
            ])

    def _format_date(self, date):
        return strptime(date, "%Y-%m-%d")





