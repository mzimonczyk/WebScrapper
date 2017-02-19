# -*- coding: utf-8 -*-

import logging
import re
from bs4 import BeautifulSoup
from DataParser import DataParser
from time import strptime


class AzairParser(DataParser):
    def __init__(self, timestamp):
        columns = ['TIMESTAMP',
                   'DEPARTURE', 'THERE_DEPARTURE_TIME', 'THERE_ARRIVAL_TIME', 'THERE_AIRLINE', 'THERE_PRICE',
                   'DESTINATION', 'BACK_DEPARTURE_TIME', 'BACK_ARRIVAL_TIME', 'BACK_AIRLINE', 'BACK_PRICE',
                   'PRICE']
        table_name = 'AZAIR'
        DataParser.__init__(self, timestamp, table_name, columns)

    def parse_data(self, content):
        content = self._correct_known_html_errors(content)
        soup = BeautifulSoup(content, 'html.parser')

        results = soup.find_all("div", class_='text')
        for result in results:
            self._parse_result(result)

    def _parse_result(self, data):
        # print data.prettify()
        details = data.findAll('div', attrs='detail')
        dates = data.findAll('span', attrs='date')
        prices = data.findAll('span', attrs='subPrice')
        total_price = data.find('span', attrs='sumPrice')
        if len(details) == 2 and len(dates) == 2 and len(prices) == 2:
            there = self._parse_result_detail(details[0], dates[0].text)
            back = self._parse_result_detail(details[1], dates[1].text)
            self._data.add_row([self._timestamp]
                               + there + [self._extract_price(prices[0].text)]
                               + back +  [self._extract_price(prices[1].text)]
                               + [self._extract_price(total_price.text)])

    def _parse_result_detail(self, detail, date_text):
        _from = detail.find('span', attrs='from').text
        _to = detail.find('span', attrs='to').text
        airport = self._extract_airport_name(_from)
        departure_time = self._extract_timestamp(_from, date_text)
        arrival_time = self._extract_timestamp(_to, date_text)
        #price = detail.find('span', attrs='legPrice').text
        _airline = detail.find('span', attrs='airline')
        airline = ''
        if _airline is not None:
            airline = _airline.text

        return [airport, departure_time, arrival_time, airline]

    def _extract_price(self, text):
        return text.replace(u' zł', u'')\
            .replace(u'Total: ', u'').strip()

    def _extract_airport_name(self, text):
        # Fr 16:20 Warsaw WAW
        results = re.match(r".*\d\d:\d\d "
                           r"(?P<AIRPORT>.*)"
                           , text, re.UNICODE)
        return results.group("AIRPORT").encode("utf-8").strip()

    def _extract_timestamp(self, text, date_text):
        # Fr 16:20 Warsaw WAW
        results = re.match(r".*(?P<TIME>\d\d:\d\d).*"
                           , text, re.UNICODE)
        time = results.group("TIME").encode("utf-8").strip()

        results = re.match(r".* (?P<DATE>\d\d/\d\d/\d\d).*"
                           , date_text, re.UNICODE)
        date = results.group("DATE").encode("utf-8").strip()
        return strptime(date + ' ' + time, "%d/%m/%y %H:%M")

    def _correct_known_html_errors(self, content):
        content = self._remove_invalid_span_closures(content)
        return content

    def _remove_invalid_span_closures(self, content):
        invalid = '<span class="icoPriceHistory" title="Price history of this flight" alt="Price history of this flight" />'
        correct = '<span class="icoPriceHistory" title="Price history of this flight" alt="Price history of this flight">'
        content = content.replace(invalid, correct)
        return content
