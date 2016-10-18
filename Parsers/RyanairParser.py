import logging
import json
import re
from DataParser import DataParser
from time import strptime


class RyanairParser(DataParser):
    def __init__(self, timestamp):
        columns = ['TIMESTAMP', 'DEPARTURE', 'DESTINATION', 'DEPARTURE_TIME', 'PRICE', 'CURRENCY']
        table_name = 'RYANAIR'
        DataParser.__init__(self, timestamp, table_name, columns)

    def parse_data(self, content):
        # data = json.loads(content)
        pass







