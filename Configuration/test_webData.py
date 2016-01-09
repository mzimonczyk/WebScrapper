from unittest import TestCase
from Configuration.WebData import WebData


class TestWebData(TestCase):
    def test_WebData_object_returns_proper_column_list(self):
        column_list = ['Type', 'name', 'address']

        web_data = WebData('TEST', column_list)

        self.assertEqual(web_data.get_columns(), column_list)

    def test_rows_are_properly_returned(self):
        column_list = ['Type', 'name', 'address']
        row1 = ['string', 'ala', 'poland']
        row2 = ['int', 'ola', 'germany']
        web_data = WebData('TEST', column_list)
        web_data.add_row(row1)
        web_data.add_row(row2)

        rows = web_data.get_rows()

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], row1)
        self.assertEqual(rows[1], row2)

    def test_add_row_throws_exception_when_invalid_row_is_passed(self):
        column_list = ['Type', 'name', 'address']
        invalid_row = ['string', 'ala', 'poland', 'high']
        web_data = WebData('TEST', column_list)

        self.assertRaises(Exception, web_data.add_row, invalid_row)