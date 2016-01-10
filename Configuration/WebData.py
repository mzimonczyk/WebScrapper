

class WebData:
    def __init__(self, table_name, column_list):
        self._table_name = table_name
        self._column_list = column_list
        self._row_list = list()

    _table_name = None
    _row_list = list()
    _column_list = None

    def get_table_name(self):
        return self._table_name

    def get_columns(self):
        return self._column_list

    def get_rows(self):
        return self._row_list

    def add_row(self, row):

        assert len(row) == len(self._column_list)
        self._row_list.append(row)

    def clear(self):
        self._row_list = list()
