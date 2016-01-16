from DataGrabber import IDataGrabber
import requests


class PostDataGrabber(IDataGrabber):
    def __init__(self):
        IDataGrabber.__init__(self)

    def get_data(self, source_description):
        page = requests.post(source_description.url, data=source_description.data, headers=source_description.headers)
        return page.content
