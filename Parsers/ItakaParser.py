# -*- coding: utf-8 -*-

import json
import logging
import re
from bs4 import BeautifulSoup
from DataParser import DataParser
from datetime import datetime
from time import strptime, mktime


class ItakaParser(DataParser):
    def __init__(self, timestamp):
        columns = ['TIMESTAMP', 'DEPARTURE', 'DESTINATION', 'DEPARTURE_TIME', 'RETURN_TIME', 'PRICE']
        table_name = 'ITAKA'
        DataParser.__init__(self, timestamp, table_name, columns)

    _page_number = 1

    def parse_data(self, content):
        data = json.loads(content)
        self._has_more_data = data['available_more_offers']
        soup = BeautifulSoup(data['offers'], 'html.parser')

        flights = soup.find_all("div", class_='flight_offer')
        for flight in flights:
            if 'oneway' not in flight['class']:
                self.parse_flight(flight)

    def modify_source_desc(self, source_desc):
        assert self._has_more_data
        self._has_more_data = False
        self._page_number += 1
        source_desc.url = re.sub('page=\d+', 'page=' + str(self._page_number), source_desc.url)

    def parse_flight(self, flight):
        description = flight.get_text()
        # description = description.encode("utf-8")
        description = re.sub('[ \s]+', ' ', description)
        self.parse_flight_description(description)

    def parse_flight_description(self, description):
        # print 'lot' ,description
        # Gdańsk (Polska)
        # Fuerteventura (Hiszpania)
        #   Bilet tam i z powrotem
        #   Wylot
        # 4 Styczeń 16:45 (Pon) Gdańsk, Rębiechowo
        #           21:30 (Pon) Fuerteventura, Puerto del Rosario
        #   Powrót
        # 18 Styczeń 08:30 (Pon) Fuerteventura, Puerto del Rosario
        #           15:55 (Pon) Gdańsk, Rębiechowo
        #   W cenie: Bagaż Opłaty lotniskowe
        #   Rezerwuj
        # 1 446pln

        # Warszawa (Polska) Barcelona (Hiszpania) Bilet tam i z powrotem Wylot
        # 9 Styczeń 05:00 (Sob) Warszawa, Okęcie 08:10 (Sob) Barcelona, Barcelona Powrót 16 Styczeń 09:00 (Sob) Barcelona, Barcelona 12:00 (Sob) Warszawa, Okęcie W cenie: Bagaż Opłaty lotniskowe Rezerwuj 391pln
        description = description.replace('--:--', '00:00')
        results = re.match(r"(?P<DEPARTURE>[ \w]+)\([\w ]+\)"
                           r"(?P<DESTINATION>[ \w]+\([\w ]+\))"
                           r".*Wylot "
                           r"(?P<DEPARTURE_DATE>.*\d\d:\d\d).*"
                           r"(?P<arrival_time>.*\d\d:\d\d).*"
                           r".*Powr.t "
                           r"(?P<RETURN_DATE>.*\d\d:\d\d).*"
                           r"(?P<return_arrival_time>.*\d\d:\d\d).*"
                           r".*Rezerwuj "
                           r"(?P<PRICE>[\d ]+)"
                           , description, re.UNICODE)
        if results:
            # print results.group("DEPARTURE").encode("utf-8"), results.groups()
            self._data.add_row([self._timestamp
                                   , results.group("DEPARTURE").encode("utf-8").strip()
                                   , results.group("DESTINATION").encode("utf-8").strip()
                                   , self.format_date(results.group("DEPARTURE_DATE"))
                                   , self.format_date(results.group("RETURN_DATE"))
                                   , results.group("PRICE").replace(' ', '')])
        else:
            logging.error('Parsing flight failed. Description: %s', description)

    def format_date(self, date):
        months = [u'zero index', u'Styczeń', u'Luty', u'Marzec', u'Kwiecień', u'Maj', u'Czerwiec', u'Lipiec',
                  u'Sierpień',
                  u'Wrzesień', u'Październik', u'Listopad', u'Grudzień']
        year = datetime.now().year
        # 9 Luty 12:30'
        results = re.match(r"(?P<day>\d+) "
                           r"(?P<month>\w+) "
                           r"(?P<hour>\d+):"
                           r"(?P<minute>\d+)"
                           , date, re.UNICODE)
        if not results:
            print 'ItakaParser.format_date. Invalid date format: ', date
        assert results
        # if results:
        #     print results.group("day"), results.group("month"), results.group("hour"), results.group("minute")

        month = months.index(results.group("month"))
        formatted_date = str(year) + '-' + str(month) + '-' + results.group("day") \
                         + ' ' + results.group("hour") + ':' + results.group("minute")

        return_date = strptime(formatted_date, "%Y-%m-%d %H:%M")
        if datetime.fromtimestamp(mktime(return_date)) < datetime.now():
            formatted_date = str(year+1) + '-' + str(month) + '-' + results.group("day") \
                         + ' ' + results.group("hour") + ':' + results.group("minute")
            return_date = strptime(formatted_date, "%Y-%m-%d %H:%M")


        return return_date