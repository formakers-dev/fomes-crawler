import unittest

from appbee_crawler.spiders.app_spider import AppSpider
from appbee_crawler.test.fake_response import fake_response

class TestAppSpider(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.spider = AppSpider()

    def test_parse_app_item_with_free_app_success_response(self):
        response = fake_response('./data/free_app_data.html')
        result = self.spider.parse_app_item(response)
        self.assertEqual(result['app_name'], '마이 오아시스 - 힐링되는 하늘섬 키우기')
        self.assertEqual(result['app_price'], 0)
        self.assertEqual(result['category_id'], '시뮬레이션')
        self.assertEqual(result['contents_rating'], '만 3세 이상')
        self.assertTrue('게임 설명' in result['description'])
        self.assertEqual(result['developer'], 'Buff Studio Co.,Ltd.')
        self.assertEqual(result['star'], 4.8)
        self.assertEqual(result['installs_min'], 100000)
        self.assertEqual(result['installs_max'], 500000)
        self.assertEqual(result['review_count'], 9783)
        self.assertEqual(result['updated_date'], "20170714")
        self.assertEqual(result['inapp_price_min'], 1000)
        self.assertEqual(result['inapp_price_max'], 100000)

    def test_parse_app_item_with_paid_app_success_response(self):
        response = fake_response('./data/paid_app_data.html')
        result = self.spider.parse_app_item(response)
        self.assertEqual(result['app_name'], '아이필터 PRO - 블루라이트 차단')
        self.assertEqual(result['app_price'], 1000)
        self.assertEqual(result['category_id'], '건강/운동')
        self.assertEqual(result['contents_rating'], '만 3세 이상')
        self.assertTrue('시력저하, 수면장애' in result['description'])
        self.assertEqual(result['developer'], 'LunaTouch')
        self.assertEqual(result['star'], 4.6)
        self.assertEqual(result['installs_min'], 50000)
        self.assertEqual(result['installs_max'], 100000)
        self.assertEqual(result['review_count'], 1036)
        self.assertEqual(result['updated_date'], "20161223")
        self.assertEqual(result['inapp_price_min'], 0)
        self.assertEqual(result['inapp_price_max'], 0)

    def test_parse_app_item_with_paid_app_failure_response(self):
        response = fake_response('./data/empty_data.html')
        result = self.spider.parse_app_item(response)
        self.assertIsNone(result)

    def test_request_similar_apps(self):
        response = fake_response('./data/free_app_data.html')
        generator = self.spider.request_similar_apps(response)
        self.assertEqual(next(generator)._get_url(), 'https://play.google.com/store/apps/details?id=com.disney.moanaislandlife_goo')
        self.assertEqual(next(generator)._get_url(), 'https://play.google.com/store/apps/details?id=com.sparklingsociety.cityislandairport2')
        self.assertEqual(next(generator)._get_url(), 'https://play.google.com/store/apps/details?id=com.astragon.cs2014')
        next(generator)
        next(generator)
        next(generator)
        next(generator)
        next(generator)
        self.assertRaises(StopIteration, next, generator)

if __name__ == '__main__':
    unittest.main()
