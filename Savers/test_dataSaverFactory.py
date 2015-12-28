from unittest import TestCase
from Savers.Factory import DataSaverFactory
from Savers.MySqlDataSaver import MySqlDataSaver
from Configuration.SourceDescription import SourceDescription


class TestDataSaverFactory(TestCase):
    def test_factory_creates_object(self):
        factory = DataSaverFactory()
        source = SourceDescription

        saver = factory.create(source)

        self.assertIsNotNone(saver)
        self.assertIsInstance(saver, MySqlDataSaver)
