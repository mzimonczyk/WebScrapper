# -*- coding: utf-8 -*-


from unittest import TestCase
from Savers.MySqlDataSaver import MySqlDataSaver
from Configuration.WebData import WebData
from Configuration.DbConfiguration import DbConfiguration


class TestMySqlDataSaver(TestCase):
    def test_get_add_query_returns_correct_query(self):
        saver = MySqlDataSaver('host', 'db', 'usr', 'pwd')
        data = WebData('TEST', ['NAME', 'AGE'])
        data.add_row(['John', '31'])

        query = saver.get_add_query(data)

        self.assertEqual(query, 'INSERT INTO TEST (NAME, AGE) VALUES (%s, %s)')

    def test_save_data_insert_data_into_database(self):
        config = DbConfiguration('config.ini')
        saver = MySqlDataSaver(config.host, config.database, config.user, config.password)
        data = WebData('TEST', ['NAME', 'SURNAME'])
        data.add_row(['Styczeń', 'Test Cityń'])

        saved = saver.save_data(data)

        self.assertTrue(saved)
