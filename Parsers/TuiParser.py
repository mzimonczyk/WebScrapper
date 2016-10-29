import logging
import json
import re
from DataParser import DataParser
from time import strptime


class TuiParser(DataParser):
    def __init__(self, timestamp):
        columns = ['TIMESTAMP', 'DEPARTURE', 'DESTINATION', 'DEPARTURE_TIME', 'RETURN_TIME', 'PRICE',
                   'FREE_SEATS', 'LAST_UPDATE']
        table_name = 'TUI'
        DataParser.__init__(self, timestamp, table_name, columns)
        self._last_row_count = 0

    _page_number = 1
    _last_row_count = 0

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
        for row in rows:
            # print row['airport_from_name'], row['airport_to_name']
            try:
                self._data.add_row([
                    self._timestamp
                    , row['airport_from_name'].strip()
                    , row['airport_to_name'].encode("utf-8").strip() + ' - '.encode("utf-8")
                      + row['country_name_to'].encode("utf-8").strip()
                    , self.format_date(row['dt_from'])
                    , self.format_date(row['dt_to'])
                    , row['price']
                    , row['free_seats']
                    , strptime(row['last_update'], "%Y-%m-%d %H:%M:%S")
                ])
            except KeyError as ex:
                logging.error('KeyError - no key: %s while parsing row: %s', type(ex), ex, row)

    def format_date(self, date):
        # dt_from=2016-06-14
        return strptime(date, "%Y-%m-%d")
