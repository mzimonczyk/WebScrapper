from unittest import TestCase
from Configuration.SourceDescription import SourceDescription
from Parsers.DoYouSpainParser import DoYouSpainParser
from Parsers.Factory import DataParserFactory


class TestDataParserFactory(TestCase):
    def test_factory_does_not_create_object_when_url_is_not_set(self):
        factory = DataParserFactory()
        source = SourceDescription
        source.url = None

        grabber = factory.create(source)

        self.assertIsNone(grabber)

    def test_factory_creates_DoYouSpainParser_when_url_contains_DoYouSpain_string (self):
        factory = DataParserFactory()
        source = SourceDescription
        source.url = 'https://DoYouSpain.com'

        parser = factory.create(source)

        self.failIfEqual(parser, None)
        self.assertIsNotNone(parser)
        self.assertIsInstance(parser, DoYouSpainParser)
