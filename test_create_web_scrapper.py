from unittest import TestCase
from WebScrapper import create_web_scrapper
from WebScrapper import WebScrapper
from Configuration.SourceDescription import SourceDescription


class TestCreateWebScrapper(TestCase):
    def test_function_creates_WebScrapper_object(self):
        source = SourceDescription()

        scrapper = create_web_scrapper(source)

        self.assertIsNotNone(scrapper)
        self.assertIsInstance(scrapper, WebScrapper)

    def test_function_creates_WebScrapper_object_with_all_members_set(self):
        source = SourceDescription()
        source.type = 'POST'
        source.url = "https://DoYouSpain.com"

        scrapper = create_web_scrapper(source)
        self.failIfEqual(scrapper, None)
        self.assertIsInstance(scrapper, WebScrapper)
        self.assertIsNotNone(scrapper._source_desc)
        self.assertIsNotNone(scrapper._grabber)
        self.assertIsNotNone(scrapper._parser)
        self.assertIsNotNone(scrapper._saver)
