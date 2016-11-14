import logging
import json
import re
from DataParser import DataParser
import datetime
from time import strptime

class RyanairParser(DataParser):
    def __init__(self, timestamp):
        columns = ['TIMESTAMP', 'DEPARTURE', 'DESTINATION', 'DEPARTURE_TIME', 'PRICE', 'REGULAR_PRICE', 'CURRENCY'
                   , 'PROMO_SEATS_LEFT']
        table_name = 'RYANAIR'
        DataParser.__init__(self, timestamp, table_name, columns)
        # set to True to download more data but your IP might be banned by ryanair
        self._has_more_data = False

    _currency = None
    _departure = None
    _destination = None
    _first_date = None

    def _get_date_and_days(self, url):
        # https://desktopapps.ryanair.com/pl-pl/availability?ADT=2&CHD=0&DateOut=2016-11-06&Destination=KTW&FlexDaysOut=6&INF=0&Origin=PLM&RoundTrip=false&TEEN=0
        params = [i.split('=') for i in url.split('&')]
        flexDaysOut = int([i[1] for i in params if i[0] == 'FlexDaysOut'][0])
        dateOut = [i[1] for i in params if i[0] == 'DateOut'][0]
        dateOut = datetime.datetime.strptime(dateOut, "%Y-%m-%d")
        return dateOut, flexDaysOut

    def _get_new_date(self, url, date):
        date_str = date.strftime("%Y-%m-%d")
        return re.sub('DateOut=\d\d\d\d-\d\d-\d\d', 'DateOut=' + date_str, url)

    def _should_proceed_more_data(self, date):
        return self._first_date is not None and date < self._first_date + datetime.timedelta(days=365)

    def modify_source_desc(self, source_desc):
        assert self._has_more_data
        self._has_more_data = False
        date, days = self._get_date_and_days(source_desc.url)
        if self._should_proceed_more_data(date):
            date = date + datetime.timedelta(days=days + 1)
            source_desc.url = self._get_new_date(source_desc.url, date)
            self._has_more_data = True

    def _parse_flight_data(self, flight):
        departure_time = strptime(flight['time'][0], "%Y-%m-%dT%H:%M:%S.000")
        if 'regularFare' in flight:
            price = flight['regularFare']['fares'][0]['amount']
            regular_price = flight['regularFare']['fares'][0]['publishedFare']
            promo_seats_left = flight['faresLeft']
            self._data.add_row([
                self._timestamp
                , self._departure
                , self._destination
                , departure_time
                , price
                , regular_price
                , self._currency
                , promo_seats_left
                ])

    def _parse_date_data(self, date_data):
        if self._first_date is None:
            self._first_date = datetime.datetime.strptime(date_data['dateOut'], "%Y-%m-%dT%H:%M:%S.000")
        if len(date_data['flights']) > 0:
            for flight in date_data['flights']:
                self._parse_flight_data(flight)

    def _parse_trips(self, trip_data):
        self._departure = trip_data['origin']
        self._destination = trip_data['destination']
        for date in trip_data['dates']:
            self._parse_date_data(date)

    def parse_data(self, content):
        data = json.loads(content)
        if 'currency' in data:
            self._currency = data['currency']
            self._parse_trips(data['trips'][0])








