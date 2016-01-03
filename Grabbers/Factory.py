from GetGrabber import GetDataGrabber
from PostGrabber import PostDataGrabber


class DataGrabberFactory:
    @staticmethod
    def create(source_description):
        if source_description.type == 'GET':
            return GetDataGrabber()
        elif source_description.type == 'POST':
            return PostDataGrabber()
        pass

