import requests
from DataGrabber import IDataGrabber


class GetDataGrabber(IDataGrabber):
    def __init__(self):
        IDataGrabber.__init__(self)

    def get_data(self, source_description):
        page = requests.get(source_description.url)
        return page.content
