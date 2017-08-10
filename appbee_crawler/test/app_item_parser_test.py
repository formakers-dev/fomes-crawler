import unittest

from appbee_crawler.spiders.parser.app_item_parser import AppItemParser
from appbee_crawler.test.fake_response import fake_response

class TestAppItemParser(unittest.TestCase):

    def setUp(self):
        super().setUp()

    def test_parse_app_item_with_free_app_success_response(self):
        response = fake_response('./data/free_app_data.html')
        result = AppItemParser.parse(response)
        self.assertEqual(result['app_name'], '마이 오아시스 - 힐링되는 하늘섬 키우기')
        self.assertEqual(result['app_price'], 0)
        self.assertEqual(result['category1_id'], '/store/apps/category/GAME_SIMULATION')
        self.assertEqual(result['category1_name'], '시뮬레이션')
        self.assertEqual(result['category2_id'], '/store/apps/category/FAMILY_ACTION')
        self.assertEqual(result['category2_name'], '액션/어드벤처')
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
        self.assertEqual(result['similar_apps'][0], "com.disney.moanaislandlife_goo")

    def test_parse_app_item_with_paid_app_success_response(self):
        response = fake_response('./data/paid_app_data.html')
        result = AppItemParser.parse(response)
        self.assertEqual(result['app_name'], '아이필터 PRO - 블루라이트 차단')
        self.assertEqual(result['app_price'], 1000)
        self.assertEqual(result['category1_id'], '/store/apps/category/HEALTH_AND_FITNESS')
        self.assertEqual(result['category1_name'], '건강/운동')
        self.assertEqual(result['category2_id'], '')
        self.assertEqual(result['category2_name'], '')
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
        self.assertEqual(result['similar_apps'][0], "com.lunatouch.eyefilter.classic")

    def test_parse_app_item_with_no_score_and_no_similar_app_success_response(self):
        response = fake_response('./data/no_score_no_similar_app_data.html')
        result = AppItemParser.parse(response)
        self.assertEqual(result['app_name'], 'Shooting Champ')
        self.assertEqual(result['app_price'], 0)
        self.assertEqual(result['category1_id'], '/store/apps/category/GAME_SPORTS')
        self.assertEqual(result['category1_name'], '스포츠')
        self.assertEqual(result['category2_id'], '')
        self.assertEqual(result['category2_name'], '')
        self.assertEqual(result['contents_rating'], '만 3세 이상')
        self.assertTrue('1대1로 과녁을' in result['description'])
        self.assertEqual(result['developer'], 'Nurida')
        self.assertEqual(result['star'], 0)
        self.assertEqual(result['installs_min'], 5)
        self.assertEqual(result['installs_max'], 10)
        self.assertEqual(result['review_count'], 0)
        self.assertEqual(result['updated_date'], "20170717")
        self.assertEqual(result['inapp_price_min'], 1200)
        self.assertEqual(result['inapp_price_max'], 120000)
        self.assertEqual(len(result['similar_apps']), 0)

    def test_parse_app_item_with_paid_app_failure_response(self):
        response = fake_response('./data/empty_data.html')
        result = AppItemParser.parse(response)
        self.assertIsNone(result)

    def test_parse_app_item_when_no_installs(self):
        response = fake_response('./data/paid_app_data_no_installs.html')
        result = AppItemParser.parse(response)
        self.assertEqual(result['installs_min'], 0)
        self.assertEqual(result['installs_max'], 5)

if __name__ == '__main__':
    unittest.main()
