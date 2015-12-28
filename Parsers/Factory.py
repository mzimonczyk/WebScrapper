from DoYouSpainParser import DoYouSpainParser
import string


class DataParserFactory:
    @staticmethod
    def create(source_description):
        if source_description is None or source_description.url is None:
            return None
        if string.find(source_description.url.lower(), 'doyouspain') >= 0:
            return DoYouSpainParser()
        pass

