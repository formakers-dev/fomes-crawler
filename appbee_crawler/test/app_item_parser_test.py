import unittest

from scrapy import Selector

from appbee_crawler.spiders.parser.app_item_parser import AppItemParser
from appbee_crawler.test.fake_response import fake_response


class ParseTestCase(unittest.TestCase):

    # data/category_data.html : Google Play Apps(https://play.google.com/store/apps) 의 카테고리 리스트
    # data/free_app_data.html : 무료앱 Detail 페이지 (리뷰점수, 유사앱, 인앱 결제 가격이 범위로 표시)
    # data/no_score_no_similar_app_data.html : 리뷰점수, 유사앱이 없는 앱의 Detail 페이지
    # data/non_range_inapp_price_data.html : 인앱 결제 가격이 한 가지인 앱의 Detail 페이지
    # data/paid_app_data.html : 유료앱 Detail 페이지

    def setUp(self):
        super().setUp()

    def test_parse_app_item_with_free_app_success_response(self):
        response = fake_response('./data/free_app_data.html', 'https://play.google.com/store/apps/details?id=jp'
                                                              '.pokemon.pokemonquest')
        result = AppItemParser.parse(response)

        self.assertEqual('포켓몬 퀘스트', result['appName'])
        self.assertEqual('jp.pokemon.pokemonquest', result['packageName'])
        self.assertEqual(0, result['appPrice'])
        self.assertEqual('GAME_ROLE_PLAYING', result['categoryId1'])
        self.assertEqual('롤플레잉', result['categoryName1'])
        self.assertEqual('FAMILY_ACTION', result['categoryId2'])
        self.assertEqual('액션/어드벤처', result['categoryName2'])
        self.assertEqual('만 3세 이상', result['contentsRating'])
        self.assertTrue('■포켓몬들이 네모나다!? 모든 것이 "네모난" 세상에 드러난 네모루루섬에서 보물을 찾아 떠나자!' in result['description'])
        self.assertEqual('The Pokemon Company', result['developer'])
        self.assertEqual(4.225265026092529, result['star'])
        self.assertEqual(5000000, result['installsMin'])
        self.assertEqual(10000000, result['installsMax'])
        self.assertEqual(85855, result['reviewCount'])
        self.assertEqual("20181206", result['updatedDate'])
        self.assertEqual(3300, result['inappPriceMin'])
        self.assertEqual(33000, result['inappPriceMax'])
        self.assertEqual("es.socialpoint.MonsterLegends", result['similarApps'][0])
        print(result['similarApps'])
        self.assertEqual("https://lh3.googleusercontent.com/EgO34BOGEhnGGd0Yk4HRppcYAF8RNF7"
                         "-WCe0Y2j6rzvn5CGQlrQj6BxaCRT5h7PdnA=s180-rw", result['iconUrl'])

        image_urls = [
            "https://lh3.googleusercontent.com/7Iof5_H6bUMcHaiOCEIPPIy-KBDX885C4RCqDEyFbyobpc-qy8DWEdLEL0m0bqIs7Pss=w720-h310-rw",
            "https://lh3.googleusercontent.com/vkE--f8u6sbzU0Smzx3eTUvAbYipaWnG0LbZk49epsqlCjByrJ09pU2ggeRHmeiWIw=w720-h310-rw",
            "https://lh3.googleusercontent.com/B4cporYV8Ix0ka7q_o5UpyPTXPYRFs4JW0fp23_wbASD3WvbAfJIf9tAN58TOgZ_-Bkt=w720-h310-rw",
            "https://lh3.googleusercontent.com/vMkZoD7TZkc355RUjXDhw-NWvyaa2PMTe2_kedQNvh4KIlGoecoSjObKLVr-POTKCxcG=w720-h310-rw",
            "https://lh3.googleusercontent.com/zsrWQZHHPGUJWV2dg7gp47WaOVpNpB9A03l5U-pf27UBLG0eqYNWFzTbuBctPhHed_Y=w720-h310-rw",
            "https://lh3.googleusercontent.com/ruvuTMtHavwKUUusNKAN2pb_D_ZxniMB4gw8tVMQ0d-XMaAadIQQpt8VlF8GlIzOxO3j=w720-h310-rw",
            "https://lh3.googleusercontent.com/Tv7Slw91501-6SIxrwQkAQ4aUcQ1OWcU8fbHHlucsI9ehfmEPZooJuOc9e_Yz0H5piwz=w720-h310-rw",
            "https://lh3.googleusercontent.com/x8FytN5oDAfm8ujGDVnVttm8LrYF-oJn26cp-F6A2K31VPdW5_-JCefjYNZeikurc98=w720-h310-rw",
            "https://lh3.googleusercontent.com/ILYPQsMHOHFtBt6Yh5xg2W5iQD1F3lebXomX0Wka3tAthMxJHkfXJQQQReLJn3f1gog=w720-h310-rw",
            "https://lh3.googleusercontent.com/Ygar-ngJyF7-X2s_yyDdCRxWh9RfqJcux0iZ4O1nx5lhyhl5BdcId5vdBeaRatGwoyI=w720-h310-rw",
            "https://lh3.googleusercontent.com/_HsdPosWctr8A8hkc7Wc1Q4Uu_MoYHjMcgBiNjVCH0tuKuyafzuuxQJI8gFi45twqgw=w720-h310-rw",
            "https://lh3.googleusercontent.com/kDuIwnAo-SepPfepgk_Hhota6aoVqW51DSTCv5N7H_57CuP5FWWjSbccnAvP4fPjWyk=w720-h310-rw",
        ]
        self.assertEqual(image_urls, result['imageUrls'])

    def test_parse_app_item_with_paid_app_success_response(self):
        response = fake_response('./data/paid_app_data.html', 'https://play.google.com/store/apps/details?id=com'
                                                              '.lunatouch.eyefilter.pro')
        result = AppItemParser.parse(response)
        self.assertEqual('아이필터 PRO - 블루라이트 차단', result['appName'])
        self.assertEqual('com.lunatouch.eyefilter.pro', result['packageName'])
        self.assertEqual(2000, result['appPrice'])  # 가격
        self.assertEqual('HEALTH_AND_FITNESS', result['categoryId1'])
        self.assertEqual('건강/운동', result['categoryName1'])
        self.assertEqual('', result['categoryId2'])
        self.assertEqual('', result['categoryName2'])
        self.assertEqual('만 3세 이상', result['contentsRating'])
        self.assertTrue('시력저하, 수면장애' in result['description'])
        self.assertEqual('Media Life Inc', result['developer'])
        self.assertEqual(3.887596845626831, result['star'])
        self.assertEqual(50000, result['installsMin'])
        self.assertEqual(100000, result['installsMax'])
        self.assertEqual(2578, result['reviewCount'])
        self.assertEqual("20180528", result['updatedDate'])
        self.assertEqual(0, result['inappPriceMin'])
        self.assertEqual(0, result['inappPriceMax'])
        self.assertEqual("com.lunatouch.eyefilter.free", result['similarApps'][0])
        self.assertEqual("https://lh3.googleusercontent.com"
                         "/uTXhW9YVTDdkJg5JaSDyjnjg0UFRolcuor9uq4fhYBbNgzyT3I8ZFQG2HwODAMlZUPo=s180-rw",
                         result['iconUrl'])

        image_urls = [
            'https://lh3.googleusercontent.com/2SQ_WYgDzeY17Q8JqXT5XHBAYAdxxe-1hcY2EDO79R07R-OylMV58THw1nOwFhDomFY=w720-h310-rw',
            'https://lh3.googleusercontent.com/aiiR0QMf-3-07wMIa0e3MaCg-AKB2eFJ84FJGklMqkGVfp5222tQnMY-MgJxRX9wbA=w720-h310-rw',
            'https://lh3.googleusercontent.com/0b5okCg8BxzJ2ApWF3hFD29QOmscZocMU1pFypDVsRTEuTRq-at4_Ty9Ja8ol4ooqQru=w720-h310-rw',
            'https://lh3.googleusercontent.com/3bCclcU-4koSyS6idZCJ0ZO-sKRhBZXVHM1K5eQphtBUbYPlqOnAchFPZlfVnpk-o-8=w720-h310-rw',
            'https://lh3.googleusercontent.com/zi-7L0HdYTR6mUV__0MYD6cevggaCvZ0keAfOGGAAuw7IidQP3ZpOzCPlkZ96mR0Xw=w720-h310-rw',
            'https://lh3.googleusercontent.com/2N_YKAKH0jNUI7xDPaB-pWWfl8_h5mwH5gELkeSjTRhdC5DE5WAxCH8PbFziVOGS3CYq=w720-h310-rw',
            'https://lh3.googleusercontent.com/MwFL33dFkt8G01xnjgVw7bFWcBTE8nQLifb3zBMkC2ofzD46mqWgvo4xN_pEfIgQt0U=w720-h310-rw',
            'https://lh3.googleusercontent.com/3UU5m0P-JX7hSK0uYfEDMAKLQvUHOKCRfNZHeGCcge7jpUxWH8kd7jX8miTZSlWymW4=w720-h310-rw'
        ]
        self.assertEqual(image_urls, result['imageUrls'])

    def test_parse_app_item_with_no_score_and_no_similar_app_success_response(self):
        response = fake_response('./data/no_score_no_similar_app_data.html', 'https://play.google.com/store/apps'
                                                                             '/details?id=com.copyx.helloworld')
        result = AppItemParser.parse(response)
        self.assertEqual('Hello World!', result['appName'])
        self.assertEqual(0, result['appPrice'])
        self.assertEqual('ART_AND_DESIGN', result['categoryId1'])
        self.assertEqual('예술/디자인', result['categoryName1'])
        self.assertEqual('', result['categoryId2'])
        self.assertEqual('', result['categoryName2'])
        self.assertEqual('만 3세 이상', result['contentsRating'])
        self.assertTrue('Hello World! 화면 출력 앱' in result['description'])
        self.assertEqual('CopyX', result['developer'])
        self.assertEqual(0, result['star'])  # 리뷰
        self.assertEqual(0, result['installsMin'])
        self.assertEqual(0, result['installsMax'])
        self.assertEqual(0, result['reviewCount'])
        self.assertEqual("20180704", result['updatedDate'])
        self.assertEqual(0, result['inappPriceMin'])
        self.assertEqual(0, result['inappPriceMax'])
        self.assertEqual(0, len(result['similarApps']))  # 유사앱
        self.assertEqual('https://lh3.googleusercontent.com/3qKoMefvL'
                         '-4CUh9C0aLAnyNHbdOFKyGiegSP0BpxdKp6MZ2Qa_PnDttd2xr0fDurX-Q=s180-rw', result['iconUrl'])

        image_urls = [
            "https://lh3.googleusercontent.com/Wqwz4FIQPLI1a9oYoCO1wHo6HYt5uLPPWn_ud4N6UxJSyWmtDZCHPe536k7D6Ebv2oE=w720-h310-rw",
            "https://lh3.googleusercontent.com/wVf3rydJoywVk1ZKEgc0oX0qiwu8idaAeMEMn5ff7eydZECT909ZVHtgejUCINC0dG0=w720-h310-rw",
        ]
        self.assertEqual(image_urls, result['imageUrls'])

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
        response = fake_response('./data/non_range_inapp_price_data.html',
                                 'https://play.google.com/store/apps/details?id=com.exovoid.weather.app')
        result = AppItemParser.parse(response)
        self.assertEqual(result['inappPriceMin'], 4900)
        self.assertEqual(result['inappPriceMax'], 4900)

    def test_parse_app_item_without_app_price(self):
        response = fake_response('./data/without_app_price_data.html', 'https://play.google.com/store/apps/details?id'
                                                                       '=com.yahoo.mobile.client.android.flickr')
        result = AppItemParser.parse(response)
        self.assertEqual(result['appName'], 'Flickr')
        self.assertEqual(result['packageName'], 'com.yahoo.mobile.client.android.flickr')
        self.assertEqual(result['appPrice'], 0) # 가격


class ParseImageUrlsTestCase(unittest.TestCase):
    def test_parse_image_urls_호출시__data_src_속성이_있는_경우__해당_속성의_값을_반환한다(self):
        body = '<button><img data-src="https://lh3.googleusercontent.com/tqntm-XxlO7iZIOHJmrk3l4Go7kHK7LtaXp8F' \
               '-YLZsgchdk3xm1Y5Q5vo2UhxkcnfLU=w720-h310" data-ils="3" ' \
               'data-srcset="https://lh3.googletent.com/tqntm-XxlO7iZIOHJmrk3l4Go7kHK7LtaXp8F' \
               '-YLZsgchdk3xm1Y5Q5vo2UhxkcnfLU=w1440-h620 2x" src="data:image/gif;base64,' \
               'R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" class="T75of lxGQyd" aria-hidden="true" ' \
               'width="174" height="310" alt="스크린샷 이미지" itemprop="image"></button>' \
               '' \
               '<button><img data-src="https://lh3.googleusercontent.com' \
               '/7Orq2GIO5BJ54buOH8UX_8DlSQxLKDXz78Fe7sGxb5OsRC9eaGtXQUpJSbFsceYlCeY=w720-h310" data-ils="3" ' \
               'data-srcset="https://lh3.googleusercontent.com' \
               '/7Orq2GIO5BJ54b8UX_8DlSQxLKDXz78Fe7sGxb5OsRC9eaGtXQUpJSbFsceYlCeY=w1440-h620 2x" ' \
               'src="data:image/gif;base64,R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" class="T75of ' \
               'lxGQyd" aria-hidden="true" width="174" height="310" alt="스크린샷 이미지" itemprop="image"></button>'

        html_xpath_selector = Selector(text=body)

        image_urls = AppItemParser.parse_image_urls(html_xpath_selector)

        self.assertEqual(2, len(image_urls))
        self.assertEqual('https://lh3.googleusercontent.com/tqntm-XxlO7iZIOHJmrk3l4Go7kHK7LtaXp8F'
                         '-YLZsgchdk3xm1Y5Q5vo2UhxkcnfLU=w720-h310', image_urls[0])
        self.assertEqual('https://lh3.googleusercontent.com/7Orq2GIO5BJ54buOH8UX_8DlSQxLKDXz78Fe7s'
                         'Gxb5OsRC9eaGtXQUpJSbFsceYlCeY=w720-h310', image_urls[1])

    def test_parse_image_urls_호출시__data_src_속성이_없는_경우__src_속성의_값을_반환한다(self):
        body = '<html><body><button><img src="https://lh3.googleusercontent.com' \
               '/UO6TNZFTmlErswBxnrkhcs0BREVcl9mQrHlxzRb45lMEWQMIpuZBKc-Bf3QNWcyPB9U=w720-h310" ' \
               'srcset="https://lh3.googleusercontent.com/UO6TNZFTmlErswBxnrkhcs0BREVcl9mQrHlxzRb45lMEWQMIpuZBKc' \
               '-Bf3QNWcyPB9U=w1440-h620 2x" class="T75of lxGQyd" aria-hidden="true" width="174" height="310" ' \
               'alt="스크린샷 이미지" itemprop="image"></button>' \
               '' \
               '<button><img src="https://lh3.googleusercontent.com/Rs9AuPcs6prp0do-nxOglbn6ddqbS9BjOtb55qx' \
               '-18b8QwGqb9mBuSByeiF9qellRj0=w720-h310" ' \
               'srcset="https://lh3.googleusercontent.com/Rs9AuPcs6prp0lbn6ddqbS9BjOtb55qx' \
               '-18b8QwGqb9mBuSByeiF9qellRj0=w1440-h620 2x" class="T75of lxGQyd" aria-hidden="true" width="174" ' \
               'height="310" alt="스크린샷 이미지" itemprop="image"></button>'

        html_xpath_selector = Selector(text=body)

        image_urls = AppItemParser.parse_image_urls(html_xpath_selector)

        self.assertEqual(2, len(image_urls))
        self.assertEqual('https://lh3.googleusercontent.com/UO6TNZFTmlErswBxnrkhcs0BREVcl9mQrHlxzRb45lMEWQMIpuZBKc'
                         '-Bf3QNWcyPB9U=w720-h310', image_urls[0])
        self.assertEqual('https://lh3.googleusercontent.com/Rs9AuPcs6prp0do-nxOglbn6ddqbS9BjOtb55qx'
                         '-18b8QwGqb9mBuSByeiF9qellRj0=w720-h310', image_urls[1])

    # def test_parse_close_beta_app_item_success_response(self):
    #     response = fake_response('./data/close_beta_app_data.html',
    #                              'https://play.google.com/store/apps/details?id=com.mavo.moon_shooter')
    #
    #     print(AppItemParser.parse(response))


if __name__ == '__main__':
    unittest.main()
