from unittest import TestCase
from Configuration.SourceDescription import SourceDescription
from Grabbers.Factory import DataGrabberFactory
from Grabbers.PostGrabber import PostDataGrabber


class TestDataGrabberFactory(TestCase):
    def test_factory_does_not_create_object_when_type_is_not_set(self):
        factory = DataGrabberFactory()
        source = SourceDescription
        source.type = None

        grabber = factory.create(source)

        self.assertIsNone(grabber)

    def test_factory_creates_post_data_grabber_when_post_param_is_set (self):
        factory = DataGrabberFactory()
        source = SourceDescription
        source.type = 'POST'

        grabber = factory.create(source)

        self.assertIsNotNone(grabber)
        self.assertIsInstance(grabber, PostDataGrabber)

