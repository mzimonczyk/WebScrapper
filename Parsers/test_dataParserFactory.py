from unittest import TestCase

from Configuration.SourceDescription import SourceDescription
from Parsers.DoYouSpainParser import DoYouSpainParser
from Parsers.Factory import DataParserFactory
from Parsers.ItakaParser import ItakaParser
from Parsers.NorwegianFlightParser import NorwegianFlightParser
from Parsers.TuiParser import TuiParser
from Parsers.WizzairParser import WizzairParser
from Parsers.RainbowParser import RainbowParser
from Parsers.RyanairParser import RyanairParser
from Parsers.AzairParser import AzairParser
import time

#TODO add testing method to remove duplicate code

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

    def test_factory_creates_RainbowParser_when_url_contains_biletyczarterowe_r_pl_string(self):
        factory = DataParserFactory()
        source = SourceDescription
        source.url = 'http://biletyczarterowe.r.pl/Wyszukiwanie?&miastaWylotuZ=["KTW"]&miastaWylotuDo=["TFS"]'

        parser = factory.create(source)

        self.failIfEqual(parser, None)
        self.assertIsNotNone(parser)
        self.assertIsInstance(parser, RainbowParser)

    def test_factory_creates_RyanairParser_when_url_contains_ryanair_com_string(self):
        factory = DataParserFactory()
        source = SourceDescription
        source.url = 'https://www.ryanair.com/pl/api/2/flights/from/BVA/to/OPO/2016-06-01/2018-07-02/outbound/cheapest-per-day/'

        parser = factory.create(source)

        self.failIfEqual(parser, None)
        self.assertIsNotNone(parser)
        self.assertIsInstance(parser, RyanairParser)

    def test_factory_creates_AzAirParser_when_url_contains_azair_eu_string(self):
        factory = DataParserFactory()
        source = SourceDescription
        source.url = 'http://www.azair.eu/azfin.php?tp=0&searchtype=flexi&srcAirport=Krakow+%5BKRK%5D+%28%2BKTW%2COSR%2CWRO%2CWAW%29&srcTypedText=&srcFreeTypedText=&srcMC=&srcap0=KTW&srcap2=OSR&srcap7=WRO&srcap10=WAW&srcFreeAirport=&dstAirport=Anywhere+%5BXXX%5D&dstTypedText=xx&dstFreeTypedText=&dstMC=&adults=1&children=0&infants=0&minHourStay=0%3A45&maxHourStay=16%3A30&minHourOutbound=0%3A00&maxHourOutbound=24%3A00&minHourInbound=0%3A00&maxHourInbound=24%3A00&depdate=27.4.2017&arrdate=9.5.2017&minDaysStay=7&maxDaysStay=12&nextday=0&autoprice=true&currency=PLN&wizzxclub=false&supervolotea=false&schengen=false&transfer=false&samedep=true&samearr=true&dep0=true&dep1=true&dep2=true&dep3=true&dep4=true&dep5=true&dep6=true&arr0=true&arr1=true&arr2=true&arr3=true&arr4=true&arr5=true&arr6=true&maxChng=0&isOneway=return&resultSubmit=Search#'

        parser = factory.create(source)

        self.failIfEqual(parser, None)
        self.assertIsNotNone(parser)
        self.assertIsInstance(parser, AzairParser)