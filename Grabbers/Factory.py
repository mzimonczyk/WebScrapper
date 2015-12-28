from PostGrabber import PostDataGrabber


class DataGrabberFactory:
    @staticmethod
    def create(source_description):
        if source_description.type == 'POST':
            return PostDataGrabber()
        pass

