import unittest

from appbee_crawler.spiders.app_spider import AppSpider
from appbee_crawler.test.fake_response import fake_response

class TestAppSpider(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.spider = AppSpider()

    def test_after_parsing_with_free_app_success_response(self):
        response = fake_response('./data/free_app_data.html')
        result = self.spider.after_parsing(response)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['app_name'], '마이 오아시스 - 힐링되는 하늘섬 키우기')
        self.assertEqual(result[0]['app_price'], 0)
        self.assertEqual(result[0]['category_id'], '시뮬레이션')
        self.assertEqual(result[0]['contents_rating'], '만 3세 이상')
        self.assertTrue('게임 설명' in result[0]['description'])
        self.assertEqual(result[0]['developer'], 'Buff Studio Co.,Ltd.')
        self.assertEqual(result[0]['star'], '4.8')
        self.assertEqual(result[0]['installs_min'], '100000')
        self.assertEqual(result[0]['installs_max'], '500000')
        self.assertEqual(result[0]['reviews'], '9783')
        self.assertEqual(result[0]['updated'], "20170714")
        self.assertEqual(result[0]['inapp_price_min'], 1000)
        self.assertEqual(result[0]['inapp_price_max'], 100000)

    def test_after_parsing_with_paid_app_success_response(self):
        response = fake_response('./data/paid_app_data.html')
        result = self.spider.after_parsing(response)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['app_name'], '아이필터 PRO - 블루라이트 차단')
        self.assertEqual(result[0]['app_price'], 1000)
        self.assertEqual(result[0]['category_id'], '건강/운동')
        self.assertEqual(result[0]['contents_rating'], '만 3세 이상')
        self.assertTrue('시력저하, 수면장애' in result[0]['description'])
        self.assertEqual(result[0]['developer'], 'LunaTouch')
        self.assertEqual(result[0]['star'], '4.6')
        self.assertEqual(result[0]['installs_min'], '50000')
        self.assertEqual(result[0]['installs_max'], '100000')
        self.assertEqual(result[0]['reviews'], '1036')
        self.assertEqual(result[0]['updated'], "20161223")
        self.assertEqual(result[0]['inapp_price_min'], 0)
        self.assertEqual(result[0]['inapp_price_max'], 0)

    def test_after_parsing_with_paid_app_failure_response(self):
        response = fake_response('./data/empty_data.html')
        result = self.spider.after_parsing(response)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
