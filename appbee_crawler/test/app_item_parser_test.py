import unittest

from appbee_crawler.spiders.parser.app_item_parser import AppItemParser
from appbee_crawler.test.fake_response import fake_response

class TestAppItemParser(unittest.TestCase):

    def setUp(self):
        super().setUp()

    def test_parse_app_item_with_free_app_success_response(self):
        response = fake_response('./data/free_app_data.html')
        result = AppItemParser.parse(response)
        self.assertEqual(result['appName'], '마이 오아시스 - 힐링되는 하늘섬 키우기')
        self.assertEqual(result['appPrice'], 0)
        self.assertEqual(result['categoryId1'], '/store/apps/category/GAME_SIMULATION')
        self.assertEqual(result['categoryName1'], '시뮬레이션')
        self.assertEqual(result['categoryId2'], '/store/apps/category/FAMILY_ACTION')
        self.assertEqual(result['categoryName2'], '액션/어드벤처')
        self.assertEqual(result['contentsRating'], '만 3세 이상')
        self.assertTrue('게임 설명' in result['description'])
        self.assertEqual(result['developer'], 'Buff Studio Co.,Ltd.')
        self.assertEqual(result['star'], 4.8)
        self.assertEqual(result['installsMin'], 100000)
        self.assertEqual(result['installsMax'], 500000)
        self.assertEqual(result['reviewCount'], 9783)
        self.assertEqual(result['updatedDate'], "20170714")
        self.assertEqual(result['inappPriceMin'], 1000)
        self.assertEqual(result['inappPriceMax'], 100000)
        self.assertEqual(result['similarApps'][0], "com.disney.moanaislandlife_goo")
        self.assertEqual(result['iconUrl'], "https://lh3.googleusercontent.com/sPn6xnEWTfCNKJAu73s6LZw5-nzy584LbBsfkpzcD49NsyZQ75SANuuGTXDmaQp3QXY=w300-rw")

    def test_parse_app_item_with_paid_app_success_response(self):
        response = fake_response('./data/paid_app_data.html')
        result = AppItemParser.parse(response)
        self.assertEqual(result['appName'], '아이필터 PRO - 블루라이트 차단')
        self.assertEqual(result['appPrice'], 1000)
        self.assertEqual(result['categoryId1'], '/store/apps/category/HEALTH_AND_FITNESS')
        self.assertEqual(result['categoryName1'], '건강/운동')
        self.assertEqual(result['categoryId2'], '')
        self.assertEqual(result['categoryName2'], '')
        self.assertEqual(result['contentsRating'], '만 3세 이상')
        self.assertTrue('시력저하, 수면장애' in result['description'])
        self.assertEqual(result['developer'], 'LunaTouch')
        self.assertEqual(result['star'], 4.6)
        self.assertEqual(result['installsMin'], 50000)
        self.assertEqual(result['installsMax'], 100000)
        self.assertEqual(result['reviewCount'], 1036)
        self.assertEqual(result['updatedDate'], "20161223")
        self.assertEqual(result['inappPriceMin'], 0)
        self.assertEqual(result['inappPriceMax'], 0)
        self.assertEqual(result['similarApps'][0], "com.lunatouch.eyefilter.classic")
        self.assertEqual(result['iconUrl'], "https://lh3.googleusercontent.com/30K7UPWRRA6p0-fNJjbGM2HlX1PYpcnxKGUU3f4mruRn0LqHrlZ0ANOSoMGdNDWRBMY=w300-rw")

    def test_parse_app_item_with_no_score_and_no_similar_app_success_response(self):
        response = fake_response('./data/no_score_no_similar_app_data.html')
        result = AppItemParser.parse(response)
        self.assertEqual(result['appName'], 'Shooting Champ')
        self.assertEqual(result['appPrice'], 0)
        self.assertEqual(result['categoryId1'], '/store/apps/category/GAME_SPORTS')
        self.assertEqual(result['categoryName1'], '스포츠')
        self.assertEqual(result['categoryId2'], '')
        self.assertEqual(result['categoryName2'], '')
        self.assertEqual(result['contentsRating'], '만 3세 이상')
        self.assertTrue('1대1로 과녁을' in result['description'])
        self.assertEqual(result['developer'], 'Nurida')
        self.assertEqual(result['star'], 0)
        self.assertEqual(result['installsMin'], 5)
        self.assertEqual(result['installsMax'], 10)
        self.assertEqual(result['reviewCount'], 0)
        self.assertEqual(result['updatedDate'], "20170717")
        self.assertEqual(result['inappPriceMin'], 1200)
        self.assertEqual(result['inappPriceMax'], 120000)
        self.assertEqual(len(result['similarApps']), 0)
        self.assertEqual(result['iconUrl'], "https://lh3.googleusercontent.com/JSW1CJ3aJDvWh-schLVT0DTwY3EpoDwady8jnMusrHMk1zse2k0eENc5XmyQBcoMxAc=w300-rw")

    def test_parse_app_item_with_paid_app_failure_response(self):
        response = fake_response('./data/empty_data.html')
        result = AppItemParser.parse(response)
        self.assertIsNone(result)

    def test_parse_app_item_when_no_installs(self):
        response = fake_response('./data/paid_app_data_no_installs.html')
        result = AppItemParser.parse(response)
        self.assertEqual(result['installsMin'], 0)
        self.assertEqual(result['installsMax'], 5)

if __name__ == '__main__':
    unittest.main()
