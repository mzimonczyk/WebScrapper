import string
from time import strftime
from DoYouSpainParser import DoYouSpainParser
from ItakaParser import ItakaParser


class DataParserFactory:
    @staticmethod
    def create(source_description):
        if source_description is None or source_description.url is None:
            return None
        elif string.find(source_description.url.lower(), 'doyouspain') >= 0:
            return DoYouSpainParser()
        elif string.find(source_description.url.lower(), 'itaka.pl') >= 0:
            return ItakaParser(strftime("%Y-%m-%d %H:%M:%S"))
        pass

