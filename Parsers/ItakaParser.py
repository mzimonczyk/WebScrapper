# -*- coding: utf-8 -*-

import json
import re

from bs4 import BeautifulSoup

from DataParser import IDataParser


class ItakaParser(IDataParser):
    def __init__(self):
        IDataParser.__init__(self)

    _has_more_data = False
    _page_number = 1

    def parse_data(self, content):
        data = json.loads(content)
        self._has_more_data = data['available_more_offers']
        soup = BeautifulSoup(data['offers'], 'html.parser')

        flights = soup.find_all("div", class_='flight_offer')
        for flight in flights:
            if 'oneway' not in flight['class']:
                self.parse_flight(flight)
                # return
        pass

    def get_data(self):
        return [None]

    def has_more_data(self):
        return self._has_more_data

    def modify_source_desc(self, source_desc):
        assert self._has_more_data
        self._has_more_data = False
        self._page_number += 1
        source_desc.url = re.sub('page=\d+', 'page=' + str(self._page_number), source_desc.url)

    def parse_flight(self, flight):
        description = flight.get_text()
        description = re.sub('[ \s]+', ' ', description)
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

        results = re.match(r"(?P<from>[ \w]+)\([\w ]+\)"
                           r"(?P<to>[ \w]+\([\w ]+\))"
                           r".*Wylot "
                           r"(?P<date_from_start>.*\d\d:\d\d).*"
                           r"(?P<date_from_stop>.*\d\d:\d\d).*"
                           r".*Powr.t "
                           r"(?P<date_back_start>.*\d\d:\d\d).*"
                           r"(?P<date_back_stop>.*\d\d:\d\d).*"
                           r".*Rezerwuj "
                           r"(?P<price>[\d ]+)"
                           , description, re.UNICODE)
        print results.groups()
