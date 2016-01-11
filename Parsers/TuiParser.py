from DataParser import IDataParser
import re
import json
from time import strptime
from Configuration.WebData import WebData


class TuiParser(IDataParser):
    def __init__(self, timestamp):
        IDataParser.__init__(self)
        columns = ['TIMESTAMP', 'DEPARTURE', 'DESTINATION', 'COUNTRY', 'DEPARTURE_DATE', 'RETURN_DATE', 'PRICE',
                   'FREE_SEATS', 'LAST_UPDATE']
        table_name = 'TUI'
        self._data = WebData(table_name, columns)
        self._timestamp = timestamp
        self._last_row_count = 0

    _timestamp = None
    _has_more_data = False
    _page_number = 1
    _data = None
    _last_row_count = 0

    def get_data(self):
        return self._data

    def has_more_data(self):
        return self._has_more_data

    def modify_source_desc(self, source_desc):
        assert self._has_more_data
        self._has_more_data = False
        self._page_number += self._last_row_count
        source_desc.url = re.sub('page=\d+', 'page=' + str(self._page_number), source_desc.url)

    def parse_data(self, content):
        data = json.loads(content)
        self._has_more_data = data['count'] > self._page_number
        rows = data['rows']
        self._last_row_count = len(rows)
        print 'TUI page:', self._page_number, len(rows)
        for row in rows:
            # print row['airport_from_name'], row['airport_to_name']
            self._data.add_row([
                self._timestamp
                , row['airport_from_name']
                , row['airport_to_name']
                , row['country_name_to'].encode("utf-8")
                , self.format_date(row['dt_from'])
                , self.format_date(row['dt_to'])
                , row['price']
                , row['free_seats']
                , strptime(row['last_update'], "%Y-%m-%d %H:%M:%S")
            ])

    def format_date(self, date):
        # dt_from=2016-06-14
        return strptime(date, "%Y-%m-%d")
