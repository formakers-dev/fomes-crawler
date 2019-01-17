import unittest
from unittest.mock import patch, Mock

from appbee_crawler.app_items import AppItem
from appbee_crawler.spiders.app_spider import AppSpider
from appbee_crawler.spiders.parser.app_item_parser import AppItemParser
from appbee_crawler.test.fake_response import fake_response


class RequestSimilarAppsTestCase(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.spider = AppSpider()

    def test_request_similar_apps(self):
        response = fake_response('./data/free_app_data.html')
        generator = self.spider.request_similar_apps(response)
        self.assertEqual(next(generator)._get_url(),
                         'https://play.google.com/store/apps/details?id=com.idleif.abyssrium')
        self.assertEqual(next(generator)._get_url(),
                         'https://play.google.com/store/apps/details?id=com.ThreeCatGames.ThisCell')
        self.assertEqual(next(generator)._get_url(),
                         'https://play.google.com/store/apps/details?id=com.crowdstar.covetHome')
        next(generator)
        next(generator)
        self.assertRaises(StopIteration, next, generator)


class AfterParsingTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.spider = AppSpider()
        cls.game_app_item = AppItem()
        cls.game_app_item['categoryId1'] = "GAME_PUZZLE"
        cls.other_app_item = AppItem()
        cls.other_app_item['categoryId1'] = "TOOLS"

    @patch.object(AppItemParser, 'parse')
    def test_after_parsing_호출시__앱정보를_파싱한다(self, mock_parse):
        mock_parse.return_value = self.game_app_item

        generator = self.spider.after_parsing(response="test response")

        next(generator)
        mock_parse.assert_called_with("test response")

    @patch.object(AppItemParser, 'parse')
    def test_after_parsing_호출시__파싱한_앱정보를_반환한다(self, mock_parse):
        mock_parse.return_value = self.game_app_item

        mock_request_similar_apps = Mock()
        mock_request_similar_apps.return_value = iter(["similar_app_request"])

        self.spider.request_similar_apps = mock_request_similar_apps

        generator = self.spider.after_parsing(response="test_response")

        self.assertEqual("GAME_PUZZLE", next(generator)['categoryId1'])
        self.assertEqual("similar_app_request", next(generator))

    @patch.object(AppItemParser, 'parse')
    def test_after_parsing_호출시__파싱한_앱정보_중_일반앱정보는_반환하지않는다(self, mock_parse):
        mock_parse.return_value = self.other_app_item

        mock_request_similar_apps = Mock()
        mock_request_similar_apps.return_value = iter(["similar_app_request"])

        self.spider.request_similar_apps = mock_request_similar_apps

        generator = self.spider.after_parsing(response="test_response")

        self.assertEqual("similar_app_request", next(generator))


if __name__ == '__main__':
    unittest.main()
