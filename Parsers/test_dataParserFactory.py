from unittest import TestCase

from Configuration.SourceDescription import SourceDescription
from Parsers.DoYouSpainParser import DoYouSpainParser
from Parsers.Factory import DataParserFactory
from Parsers.ItakaParser import ItakaParser
from Parsers.NorwegianFlightParser import NorwegianFlightParser
from Parsers.TuiParser import TuiParser
from Parsers.WizzairParser import WizzairParser
import time


class TestDataParserFactory(TestCase):
    def test_factory_does_not_create_object_when_url_is_not_set(self):
        factory = DataParserFactory()
        source = SourceDescription
        source.url = None

        grabber = factory.create(source)

        self.assertIsNone(grabber)

    def test_factory_creates_DoYouSpainParser_when_url_contains_DoYouSpain_string(self):
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

    def test_factory_creates_all_parsers_with_the_same_timestamp(self):
        factory = DataParserFactory()
        source1 = SourceDescription
        source1.url = 'http://biletylotnicze.itaka.pl'
        source2 = SourceDescription
        source2.url = 'http://oferty.tui.pl/ajax/chartersSearch,12755?adults=2&page=5'

        parser1 = factory.create(source1)
        time.sleep(2)
        parser2 = factory.create(source2)

        self.assertEqual(parser1._timestamp, parser2._timestamp)

    def test_factory_creates_NorwegianFlightParser_when_url_contains_norwegian_wybierz_lot_string(self):
        factory = DataParserFactory()
        source = SourceDescription
        source.url = 'https://www.norwegian.com/pl/rezerwacja/zarezerwuj-przelot/wybierz-lot' \
                     '/?D_City=GDN&A_City=EVE&D_SelectedDay=04&D_Day=04&D_Month=201607&R_SelectedDay=14' \
                     '&R_Day=14&R_Month=201607&dFare=595&rFare=421&AgreementCodeFK=-1&CurrencyCode=PLN'

        parser = factory.create(source)

        self.failIfEqual(parser, None)
        self.assertIsNotNone(parser)
        self.assertIsInstance(parser, NorwegianFlightParser)

    def test_factory_creates_NorwegianFlightsParser_when_url_contains_norwegian_zarezerwuj_przelot_string(self):
        factory = DataParserFactory()
        source = SourceDescription
        source.url = 'https://www.norwegian.com/pl/rezerwacja/zarezerwuj-przelot/tanie-polaczenia/' \
                     '?D_City=GDN&A_City=EVE&D_Day=01&D_Month=201607&R_Day=01&R_Month=201607' \
                     '&AgreementCodeFK=-1&CurrencyCode=PLN'

        parser = factory.create(source)

        #self.failIfEqual(parser, None)
        self.assertIsNone(parser)

    def test_factory_creates_WizzairParser_when_url_contains_wizzair_com_string(self):
        factory = DataParserFactory()
        source = SourceDescription
        source.url = 'https://wizzair.com/pl-PL/TimeTableAjax?departureIATA=GDN&arrivalIATA=AES&year=2016&month=7'

        parser = factory.create(source)

        self.failIfEqual(parser, None)
        self.assertIsNotNone(parser)
        self.assertIsInstance(parser, WizzairParser)