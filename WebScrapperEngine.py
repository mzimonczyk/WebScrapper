from Configuration.ConfigReader import ceate_mock_config_reader
from WebScrapper import create_web_scrapper


class WebScrapperEngine:
    def __init__(self):
        self._configReader = ceate_mock_config_reader()

    _configReader = None

    def run(self):
        self._configReader.read_data()
        for data in self._configReader.get_data():
            scrapper = create_web_scrapper(data)
            scrapper.run()


if __name__ == '__main__':
    engine = WebScrapperEngine()
    engine.run()
