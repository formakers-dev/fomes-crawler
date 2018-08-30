import unittest

from appbee_crawler.spiders.parser.app_item_parser import AppItemParser
from appbee_crawler.test.fake_response import fake_response


class TestAppItemParser(unittest.TestCase):

    # data/category_data.html : Google Play Apps(https://play.google.com/store/apps) 의 카테고리 리스트
    # data/free_app_data.html : 무료앱 Detail 페이지
    # data/no_score_no_similar_app_data.html : 리뷰점수, 유사앱이 없는 앱의 Detail 페이지
    # data/non_range_inapp_price_data.html : 인앱 결제 가격이 한 가지인 앱의 Detail 페이지
    # data/paid_app_data.html : 유료앱 Detail 페이지

    def setUp(self):
        super().setUp()

    def test_parse_app_item_with_free_app_success_response(self):
        response = fake_response('./data/free_app_data.html', 'https://play.google.com/store/apps/details?id=com'
                                                              '.buffstudio.myoasis')
        result = AppItemParser.parse(response)
        self.assertEqual(result['appName'], '마이 오아시스 - 힐링되는 하늘섬 키우기')
        self.assertEqual(result['packageName'], 'com.buffstudio.myoasis')
        self.assertEqual(result['appPrice'], 0)
        self.assertEqual(result['categoryId1'], 'GAME_SIMULATION')
        self.assertEqual(result['categoryName1'], '시뮬레이션')
        self.assertEqual(result['categoryId2'], 'FAMILY_ACTION')
        self.assertEqual(result['categoryName2'], '액션/어드벤처')
        self.assertEqual(result['contentsRating'], '만 3세 이상')
        self.assertTrue('탭해서 하트를 모아 다양한 동물들이 뛰노는 오아시스' in result['description'])
        self.assertEqual(result['developer'], 'Buff Studio Co.,Ltd.')
        self.assertEqual(result['star'], 4.649204254150391)
        self.assertEqual(result['installsMin'], 1000000)
        self.assertEqual(result['installsMax'], 5000000)
        self.assertEqual(result['reviewCount'], 99833)
        self.assertEqual(result['updatedDate'], "20180629")
        self.assertEqual(result['inappPriceMin'], 1100)
        self.assertEqual(result['inappPriceMax'], 110000)
        self.assertEqual(result['similarApps'][0], "com.idleif.abyssrium")
        self.assertEqual(result['iconUrl'], "https://lh3.googleusercontent.com/OJ12eDDC6zShVguWb2mBS"
                                            "--cdUDRy4BzyqR_BfTy8kG5ibNwsbYbibNUnEW-hxUMlUM=s180")

    def test_parse_app_item_with_paid_app_success_response(self):
        response = fake_response('./data/paid_app_data.html', 'https://play.google.com/store/apps/details?id=com'
                                                              '.lunatouch.eyefilter.pro')
        result = AppItemParser.parse(response)
        self.assertEqual(result['appName'], '아이필터 PRO - 블루라이트 차단')
        self.assertEqual(result['packageName'], 'com.lunatouch.eyefilter.pro')
        self.assertEqual(result['appPrice'], 2000) # 가격
        self.assertEqual(result['categoryId1'], 'HEALTH_AND_FITNESS')
        self.assertEqual(result['categoryName1'], '건강/운동')
        self.assertEqual(result['categoryId2'], '')
        self.assertEqual(result['categoryName2'], '')
        self.assertEqual(result['contentsRating'], '만 3세 이상')
        self.assertTrue('시력저하, 수면장애' in result['description'])
        self.assertEqual(result['developer'], 'Media Life Inc')
        self.assertEqual(result['star'], 4.594583988189697)
        self.assertEqual(result['installsMin'], 50000)
        self.assertEqual(result['installsMax'], 100000)
        self.assertEqual(result['reviewCount'], 2548)
        self.assertEqual(result['updatedDate'], "20180528")
        self.assertEqual(result['inappPriceMin'], 0)
        self.assertEqual(result['inappPriceMax'], 0)
        self.assertEqual(result['similarApps'][0], "com.ascendik.eyeshield")
        self.assertEqual(result['iconUrl'], "https://lh3.googleusercontent.com"
                                            "/uTXhW9YVTDdkJg5JaSDyjnjg0UFRolcuor9uq4fhYBbNgzyT3I8ZFQG2HwODAMlZUPo"
                                            "=s180")

    def test_parse_app_item_with_no_score_and_no_similar_app_success_response(self):
        response = fake_response('./data/no_score_no_similar_app_data.html', 'https://play.google.com/store/apps'
                                                                             '/details?id=com.copyx.helloworld')
        result = AppItemParser.parse(response)
        self.assertEqual(result['appName'], 'Hello World!')
        self.assertEqual(result['appPrice'], 0)
        self.assertEqual(result['categoryId1'], 'ART_AND_DESIGN')
        self.assertEqual(result['categoryName1'], '예술/디자인')
        self.assertEqual(result['categoryId2'], '')
        self.assertEqual(result['categoryName2'], '')
        self.assertEqual(result['contentsRating'], '만 3세 이상')
        self.assertTrue('Hello World! 화면 출력 앱' in result['description'])
        self.assertEqual(result['developer'], 'Jingi.exe')
        self.assertEqual(result['star'], 0) # 리뷰
        self.assertEqual(result['installsMin'], 0)
        self.assertEqual(result['installsMax'], 0)
        self.assertEqual(result['reviewCount'], 0)
        self.assertEqual(result['updatedDate'], "20180704")
        self.assertEqual(result['inappPriceMin'], 0)
        self.assertEqual(result['inappPriceMax'], 0)
        self.assertEqual(len(result['similarApps']), 0) # 유사앱
        self.assertEqual(result['iconUrl'], "https://lh3.googleusercontent.com/3qKoMefvL"
                                            "-4CUh9C0aLAnyNHbdOFKyGiegSP0BpxdKp6MZ2Qa_PnDttd2xr0fDurX-Q=s180")

    def test_parse_app_item_with_paid_app_failure_response(self):
        response = fake_response('./data/empty_data.html')
        result = AppItemParser.parse(response)
        self.assertIsNone(result)

    def test_parse_app_item_without_inapp_price(self):
        response = fake_response('./data/paid_app_data.html', 'https://play.google.com/store/apps/details?id=com'
                                                              '.lunatouch.eyefilter.pro')
        result = AppItemParser.parse(response)
        self.assertEqual(result['inappPriceMin'], 0)
        self.assertEqual(result['inappPriceMax'], 0)

    def test_parse_app_item_with_non_range_inapp_price(self):
        response = fake_response('./data/non_range_inapp_price_data.html', 'https://play.google.com/store/apps/details?id=com.exovoid.weather.app')
        result = AppItemParser.parse(response)
        self.assertEqual(result['inappPriceMin'], 4500)
        self.assertEqual(result['inappPriceMax'], 4500)


if __name__ == '__main__':
    unittest.main()
