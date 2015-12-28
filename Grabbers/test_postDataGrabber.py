from unittest import TestCase
from Configuration.SourceDescription import SourceDescription
from Grabbers.PostGrabber import PostDataGrabber


class TestPostDataGrabber(TestCase):
    def test_grabber_returns_data(self):
        grabber = PostDataGrabber()
        sample = SourceDescription()
        sample.type = 'POST'
        sample.url = 'https://www.doyouspain.com/formulario.asp?idioma=EN'

        content = grabber.get_data(sample)

        self.assertIsNotNone(content)
        self.assertNotEqual(len(content), 0)


