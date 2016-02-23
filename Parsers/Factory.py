import string
from time import strftime
from DoYouSpainParser import DoYouSpainParser
from ItakaParser import ItakaParser
from NorwegianFlightParser import NorwegianFlightParser
from TuiParser import TuiParser

timestamp = strftime("%Y-%m-%d %H:%M:%S")


class DataParserFactory:
    @staticmethod
    def create(source_description):
        if source_description is None or source_description.url is None:
            return None
        elif string.find(source_description.url.lower(), 'doyouspain') >= 0:
            return DoYouSpainParser()
        elif string.find(source_description.url.lower(), 'itaka.pl') >= 0:
            return ItakaParser(timestamp)
        elif string.find(source_description.url.lower(), 'tui.pl') >= 0:
            return TuiParser(timestamp)
        elif string.find(source_description.url.lower(), 'www.norwegian.com/pl/rezerwacja/zarezerwuj-przelot/wybierz-lot') >= 0:
            return NorwegianFlightParser(timestamp)
        pass

