from Grabbers.Factory import DataGrabberFactory
from Parsers.Factory import DataParserFactory
from Savers.Factory import DataSaverFactory
import logging


def create_web_scrapper(source_description):
    grabber = DataGrabberFactory.create(source_description)
    parser = DataParserFactory.create(source_description)
    saver = DataSaverFactory.create(source_description)
    return WebScrapper(source_description, grabber, parser, saver)


class WebScrapper:
    def __init__(self, source_description, grabber, parser, saver):
        self._source_desc = source_description
        self._grabber = grabber
        self._parser = parser
        self._saver = saver

    _grabber = None
    _parser = None
    _saver = None
    _source_desc = None

    def run(self):
        logging.info('Starting: %s', self._source_desc.url)
        check_for_more = True
        while check_for_more:
            content = self._grabber.get_data(self._source_desc)
            self._parser.parse_data(content)
            data = self._parser.get_data()
            check_for_more = self._parser.has_more_data()
            if check_for_more:
                self._parser.modify_source_desc(self._source_desc)

            if len(data.get_rows()) > 1000 or not check_for_more:
                self._saver.save_data(data)
                data.clear()
        logging.info('Finished: %s', self._source_desc.url)

