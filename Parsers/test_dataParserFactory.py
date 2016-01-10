from unittest import TestCase

from Configuration.SourceDescription import SourceDescription
from Parsers.DoYouSpainParser import DoYouSpainParser
from Parsers.Factory import DataParserFactory
from Parsers.ItakaParser import ItakaParser
from Parsers.TuiParser import TuiParser


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

    def test_factory_creates_ItakaParser_when_url_contains_itaka_pl_string(self):
        factory = DataParserFactory()
        source = SourceDescription
        source.url = 'http://biletylotnicze.itaka.pl'

        parser = factory.create(source)

        self.failIfEqual(parser, None)
        self.assertIsNotNone(parser)
        self.assertIsInstance(parser, ItakaParser)

    def test_factory_creates_TuiParser_when_url_contains_tui_pl_string(self):
        factory = DataParserFactory()
        source = SourceDescription
        source.url = 'http://oferty.tui.pl/ajax/chartersSearch,12755?adults=2&page=5'

        parser = factory.create(source)

        self.failIfEqual(parser, None)
        self.assertIsNotNone(parser)
        self.assertIsInstance(parser, TuiParser)
