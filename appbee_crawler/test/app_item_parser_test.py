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

        self.assertEqual(len(result['screenShotUrls']), 24);
        self.assertEqual(result['screenShotUrls'][0], "https://lh3.googleusercontent.com/TVyiUM_oGq1IRvMWdQNA-mr8Vl4WdkEqdiObLfYadyyF9OoTHSZT8AnsvYFFxffkTw=w720-h310")
        self.assertEqual(result['screenShotUrls'][1], "https://lh3.googleusercontent.com/JWAY26HZZwFGW5LwgGJaqYe5CXGePh_oLNPtRwNGZnLpa8n-MDnVeEGs0y9ALAMyNv4=w720-h310")
        self.assertEqual(result['screenShotUrls'][2], "https://lh3.googleusercontent.com/voBPYesTu9PKPvOo8VKQc15YLO3hhRO-zSr-F-d5TlJcaJllI3QFKPdoEcMpxq5Xaf4=w720-h310")
        self.assertEqual(result['screenShotUrls'][3], "https://lh3.googleusercontent.com/_NumDCQqLmaIyPgARfZgq8aCDX95HuGrEipFmFO0OKpqCtaipewaR26dPYxe7uMJyE4=w720-h310")
        self.assertEqual(result['screenShotUrls'][4], "https://lh3.googleusercontent.com/YBIrXqymvZd6Ku-0OR37ZL3x5hgASgQSyYRfksw-NdtsDxX62axU69PSAm3sNhMjeQ=w720-h310")
        self.assertEqual(result['screenShotUrls'][5], "https://lh3.googleusercontent.com/TN8pCWhmDvgeS3j7TmSjf8dik45RZ5neAyBHPey266ohEGnT9jKxf4DKi09MK57PtA0=w720-h310")
        self.assertEqual(result['screenShotUrls'][6], "https://lh3.googleusercontent.com/IHwdzTtjwy328s7ZROKlD6BrYd_rz4AdkqwVyndh7FYrmPKwvO7YAsUjJTx18v0-sEN7=w720-h310")
        self.assertEqual(result['screenShotUrls'][7], "https://lh3.googleusercontent.com/xAmO99nYMXHoaVEiDBjSnR0JoqNCPOVAhuZu_OuhzB34G4tTXMf7HEsVVmmXwW99Tw=w720-h310")
        self.assertEqual(result['screenShotUrls'][8], "https://lh3.googleusercontent.com/c3jznmIFv1YW0GfNpgSoN4JqzHjlx5xRT0FOJqWTMOUJ1C3pCNTaV3CbRv09JrRgDQY=w720-h310")
        self.assertEqual(result['screenShotUrls'][9], "https://lh3.googleusercontent.com/IhC4kiQV9lWDFY9A8RB1lT0iLddIqgDMPrhhEQ7RfgbgMyi4aqCd9yaWcanzbh7j5A=w720-h310")
        self.assertEqual(result['screenShotUrls'][10], "https://lh3.googleusercontent.com/dcJJz-gnSENQY4NIXFMj6R_dILOLxZeCF_sseR1GYH_uk72Pw6TZmdrc_AURKeKsAvaC=w720-h310")
        self.assertEqual(result['screenShotUrls'][11], "https://lh3.googleusercontent.com/rNVIv8buO5wQ2odVI7PPbkLvYzRg7weNBFrnYqUsSyrU7WAS_yhWkXLmwVudIzUnwM0=w720-h310")
        self.assertEqual(result['screenShotUrls'][12], "https://lh3.googleusercontent.com/ebfMz7010t309YhdfNE3-vQU-BmJNWEzBqfWEVycTD5SVZmyvw1tZnyKAksG8uoK7J28=w720-h310")
        self.assertEqual(result['screenShotUrls'][13], "https://lh3.googleusercontent.com/3WWHYXMLf1CLheQdD7UMUvddmzpwldG_aA3FG49BLSXtePZFeHiV4211dkQtnAlOM1TN=w720-h310")
        self.assertEqual(result['screenShotUrls'][14], "https://lh3.googleusercontent.com/bifICuleBjwY9x508VD8DCvmt6gRQw2YTsaasIy9fz1F1epKW2OQmcu_utBSyluW2aT0=w720-h310")
        self.assertEqual(result['screenShotUrls'][15], "https://lh3.googleusercontent.com/2r2hFo2a63OkDeKRLJzIGPT44eP0107i1F_MRAuIsjiuqraGMjxdYcgCBaWWpcMBAcw=w720-h310")
        self.assertEqual(result['screenShotUrls'][16], "https://lh3.googleusercontent.com/-KWWPfrJb50rtUUWqJqPkvgU21bdHh6pRtfaNofNlkRniDGdnxC3Z9WkuF6E0INMfEA=w720-h310")
        self.assertEqual(result['screenShotUrls'][17], "https://lh3.googleusercontent.com/xVIsXty8gLxgLCqRjYACP_jSeo7VHCqDPy5fZQ-vYhNYCddXMt4VAYwKtW0FFYAP78Y=w720-h310")
        self.assertEqual(result['screenShotUrls'][18], "https://lh3.googleusercontent.com/D-fN3xxkJEQgjJO52243qW2HqZ30bK8_6eV5Pf-Yv2CEs1aXYRwEFq2sy82kx9n5Vkgy=w720-h310")
        self.assertEqual(result['screenShotUrls'][19], "https://lh3.googleusercontent.com/O_2aSOHLL7ThYGQNWeeNLUD1579yA7v3EOROpSTkG5lE2Yf7cNyEmRVAttquqQf3T18=w720-h310")
        self.assertEqual(result['screenShotUrls'][20], "https://lh3.googleusercontent.com/V0t2RupUijDJdcbNJpqlBmQPKTz42rnQo5BaCAcIwyHpt_L6ELG47b53qBZzUQIU0w=w720-h310")
        self.assertEqual(result['screenShotUrls'][21], "https://lh3.googleusercontent.com/dj5Pjackv08ZgoXqP-TFhXuydT46Lfo6ZneDbM3MA3GnXijVxywq2xyZU2nAuipTpQ=w720-h310")
        self.assertEqual(result['screenShotUrls'][22], "https://lh3.googleusercontent.com/VelJwUcL9YN0lR26bfxQtskhlKeJkwuJSMZu_h7Li6-uhrldGdronFIar37-6jQKOCA=w720-h310")
        self.assertEqual(result['screenShotUrls'][23], "https://lh3.googleusercontent.com/L3u28JRmjp2i0uoZL6wXoaw-7ds9KIcM_GRC5lbJZvZh3xjOog4weZk1qJQSuyBNxjA=w720-h310")

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
        self.assertEqual(len(result['screenShotUrls']), 8);
        self.assertEqual(result['screenShotUrls'][0], "https://lh3.googleusercontent.com/2SQ_WYgDzeY17Q8JqXT5XHBAYAdxxe-1hcY2EDO79R07R-OylMV58THw1nOwFhDomFY=w720-h310")
        self.assertEqual(result['screenShotUrls'][1], "https://lh3.googleusercontent.com/aiiR0QMf-3-07wMIa0e3MaCg-AKB2eFJ84FJGklMqkGVfp5222tQnMY-MgJxRX9wbA=w720-h310")
        self.assertEqual(result['screenShotUrls'][2], "https://lh3.googleusercontent.com/0b5okCg8BxzJ2ApWF3hFD29QOmscZocMU1pFypDVsRTEuTRq-at4_Ty9Ja8ol4ooqQru=w720-h310")
        self.assertEqual(result['screenShotUrls'][3], "https://lh3.googleusercontent.com/3bCclcU-4koSyS6idZCJ0ZO-sKRhBZXVHM1K5eQphtBUbYPlqOnAchFPZlfVnpk-o-8=w720-h310")
        self.assertEqual(result['screenShotUrls'][4], "https://lh3.googleusercontent.com/zi-7L0HdYTR6mUV__0MYD6cevggaCvZ0keAfOGGAAuw7IidQP3ZpOzCPlkZ96mR0Xw=w720-h310")
        self.assertEqual(result['screenShotUrls'][5], "https://lh3.googleusercontent.com/2N_YKAKH0jNUI7xDPaB-pWWfl8_h5mwH5gELkeSjTRhdC5DE5WAxCH8PbFziVOGS3CYq=w720-h310")
        self.assertEqual(result['screenShotUrls'][6], "https://lh3.googleusercontent.com/MwFL33dFkt8G01xnjgVw7bFWcBTE8nQLifb3zBMkC2ofzD46mqWgvo4xN_pEfIgQt0U=w720-h310")
        self.assertEqual(result['screenShotUrls'][7], "https://lh3.googleusercontent.com/3UU5m0P-JX7hSK0uYfEDMAKLQvUHOKCRfNZHeGCcge7jpUxWH8kd7jX8miTZSlWymW4=w720-h310")

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

        self.assertEqual(len(result['screenShotUrls']), 2);
        self.assertEqual(result['screenShotUrls'][0], "https://lh3.googleusercontent.com/Wqwz4FIQPLI1a9oYoCO1wHo6HYt5uLPPWn_ud4N6UxJSyWmtDZCHPe536k7D6Ebv2oE=w720-h310")
        self.assertEqual(result['screenShotUrls'][1], "https://lh3.googleusercontent.com/wVf3rydJoywVk1ZKEgc0oX0qiwu8idaAeMEMn5ff7eydZECT909ZVHtgejUCINC0dG0=w720-h310")

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
