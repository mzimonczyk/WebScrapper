from Configuration.ConfigReader import ceate_mock_config_reader
from WebScrapper import create_web_scrapper
import logging
from time import strftime


class WebScrapperEngine:
    def __init__(self):
        self._configReader = ceate_mock_config_reader()

    _configReader = None

    def run(self):
        self.configure_logging()
        logging.critical('start')
        self._configReader.read_data()
        for data in self._configReader.get_data():
            scrapper = create_web_scrapper(data)
            scrapper.run()
        logging.critical('end')

    def configure_logging(self):
        file_name = './Logs/WebScrapper_' + strftime('%Y%m%d_%H%M%S') + '.log'
        format_string = '%(asctime)s %(module)s %(levelname)s %(message)s'
        logging.basicConfig(filename=file_name
                            , level=logging.DEBUG
                            , format=format_string
                            , datefmt='%Y-%m-%d %H:%M:%S')

        # define a Handler which writes INFO messages or higher to the sys.stderr
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        # tell the handler to use this format
        console.setFormatter(logging.Formatter(format_string))
        # add the handler to the root logger
        logging.getLogger('').addHandler(console)

if __name__ == '__main__':
    engine = WebScrapperEngine()
    engine.run()
