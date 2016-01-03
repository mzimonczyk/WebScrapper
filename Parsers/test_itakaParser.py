from unittest import TestCase

from Parsers.ItakaParser import ItakaParser


class TestItakaParser(TestCase):
    def test_get_data_returns_some_data_after_calling_parse_data_on_content(self):
        with open('itaka.pl_content.json') as f:
            content = f.read()

        parser = ItakaParser()

        parser.parse_data(content)
        data = parser.get_data()

        self.assertGreater(len(data), 0)

    def test_has_more_data_returns_true_after_calling_parse_data_on_content_with_json_param_available_more_offers_set(
            self):
        json_string = '{"available_more_offers":true}'
        parser = ItakaParser()

        parser.parse_data(json_string)

        self.assertTrue(parser.has_more_data())
        pass

    def test_has_more_data_returns_false_after_calling_parse_data_on_content_with_json_param_available_more_offers_set(
            self):
        json_string = '{"available_more_offers":false}'
        parser = ItakaParser()

        parser.parse_data(json_string)

        self.assertFalse(parser.has_more_data())
        pass
