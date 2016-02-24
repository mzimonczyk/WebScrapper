from Configuration.WebData import WebData
from IDataParser import IDataParser


class DataParser(IDataParser):
    def __init__(self, timestamp, table_name, columns):
        IDataParser.__init__(self)
        self._data = WebData(table_name, columns)
        self._timestamp = timestamp

    _timestamp = None
    _has_more_data = False
    _data = None

    def get_data(self):
        return self._data

    def has_more_data(self):
        return self._has_more_data
