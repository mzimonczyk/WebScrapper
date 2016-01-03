from unittest import TestCase

from Configuration.SourceDescription import SourceDescription
from Grabbers.GetGrabber import GetDataGrabber


class TestGetDataGrabber(TestCase):
    def test_grabber_returns_data(self):
        grabber = GetDataGrabber()
        sample = SourceDescription()
        sample.type = 'GET'
        sample.url = 'http://biletylotnicze.itaka.pl/charter/results-json?departure_date=03.01.2016&adults=2&children=0&sort_type=3&page=1&pages=1&total=0'

        content = grabber.get_data(sample)

        self.assertIsNotNone(content)
        self.assertNotEqual(len(content), 0)
