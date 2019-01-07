import re
import unittest

import scrapy

from appbee_crawler.app_items import AppItem
from appbee_crawler.category_items import CategoryItem
from appbee_crawler.util.string_util import StringUtil


class StringUtilTest(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.trimmedPattern = re.compile('(^[\s\uFEFF]+|[\s\uFEFF]+$)')

    def test_parse_number_호출시__입력된_숫자_문자열에서_공백과_쉼표를_제거_후_정수로_바꿔서_반환한다(self):
        self.assertEqual(StringUtil.parseNumber("100,000"), 100000)
        self.assertEqual(StringUtil.parseNumber(" 111,222,333 "), 111222333)

    def __verify_trimmed(self, obj):
        if type(obj) is str:
            self.assertEqual(self.trimmedPattern.match(obj), None)
        elif type(obj) is list:
            for item in obj:
                self.__verify_trimmed(item)
        elif type(obj) is dict or isinstance(obj, scrapy.Item):
            for value in obj.values():
                self.__verify_trimmed(value)

    def test_trim_호출시__주어진_문자열의_앞_뒤_공백문자들과_BOM문자_제거(self):
        arg_string = "\t\n\t  \r\tFAMILY_ACTION    \uFEFF \uFEFF \uFEFF"

        result = StringUtil.trim(arg_string)

        self.__verify_trimmed(result)

    def test_trim_호출시__주어진_리스트_내_모든_아이템들에_트림을_적용한다(self):
        arg_list = [
            ' 마이 오아시스 - 힐링되는 하늘섬 키우기                   \t \t \t ',
            '\n\t         com.buffstudio.myoasis \r\n\r\f',
            '\t\uFEFF\t\t     https://lh3.googleusercontent.com/voBPYesTu9PKPvOo8VKQc15YLO3hhRO-zSr-F-d5TlJcaJllI3QFKPdoEcMpxq5Xaf4=w720-h310\n\t'
        ]

        result = StringUtil.trim(arg_list)

        self.__verify_trimmed(result)

    def test_trim_호출시__주어진_딕셔너리_내_모든_값들에_트림을_적용한다(self):
        arg_dict = dict()
        arg_dict['appName'] = ' 마이 오아시스 - 힐링되는 하늘섬 키우기                   \t \t \t '
        arg_dict['packageName'] = '\n\t         com.buffstudio.myoasis \r\t        \n\f'
        arg_dict['appPrice'] = 0
        arg_dict['categoryId1'] = 'GAME_SIMULATION\n'
        arg_dict['categoryName1'] = '시뮬레이션'
        arg_dict['categoryId2'] = '\t\n\r  \r\r\r  \r FAMILY_ACTION    \uFEFF \uFEFF \uFEFF'
        arg_dict['categoryName2'] = '\n액션/어드벤처 '
        arg_dict['contentsRating'] = '  \uFEFF\ufeff \n\f\r\n만 3세 이상 '

        result = StringUtil.trim(arg_dict)

        self.__verify_trimmed(result)

    def test_trim_호출시__주어진_AppItem_내_모든_필드들에_트림을_적용한다(self):
        app_item = AppItem()
        app_item['appName'] = ' 마이 오아시스 - 힐링되는 하늘섬 키우기                   \t \t \t '
        app_item['packageName'] = '\n\t         com.buffstudio.myoasis '
        app_item['appPrice'] = 0
        app_item['categoryId1'] = 'GAME_SIMULATION\n'
        app_item['categoryName1'] = '시뮬레이션'
        app_item['categoryId2'] = ' FAMILY_ACTION    \uFEFF \uFEFF \uFEFF'
        app_item['categoryName2'] = '\n액션/어드벤처 '
        app_item['contentsRating'] = '\n만 3세 이상 '
        app_item['description'] = '\uFEFF탭해서 하트를 모아 다양한 동물들이 뛰노는 오아시스'
        app_item['developer'] = '  Buff Studio Co.Ltd.             \uFEFF\t\t'
        app_item['star'] = 4.649204254150391
        app_item['installsMin'] = 1000000
        app_item['installsMax'] = 5000000
        app_item['reviewCount'] = 99833
        app_item['updatedDate'] = "20180629    "
        app_item['inappPriceMin'] = 1100
        app_item['inappPriceMax'] = 110000
        app_item['similarApps'] = list()
        app_item['similarApps'] = []
        app_item['similarApps'].append("  com.idleif.abyssrium\t")
        app_item['similarApps'].append("\ncom.idleif.abyssrium\t")
        app_item['similarApps'].append("      com.idleif.abyssrium")
        app_item['iconUrl'] = "\t\t\t          https://lh3.googleusercontent.com/OJ12eDDC6zShVguWb2mBS--cdUDRy4BzyqR_BfTy8kG5ibNwsbYbibNUnEW-hxUMlUM=s180\n\n\n"
        app_item['imageUrls'] = []
        app_item['imageUrls'].append("https://lh3.googleusercontent.com/TVyiUM_oGq1IRvMWdQNA-mr8Vl4WdkEqdiObLfYadyyF9OoTHSZT8AnsvYFFxffkTw=w720-h310\uFEFF")
        app_item['imageUrls'].append("\uFEFF  https://lh3.googleusercontent.com/JWAY26HZZwFGW5LwgGJaqYe5CXGePh_oLNPtRwNGZnLpa8n-MDnVeEGs0y9ALAMyNv4=w720-h310  ")
        app_item['imageUrls'].append("\t\uFEFF\t\t     https://lh3.googleusercontent.com/voBPYesTu9PKPvOo8VKQc15YLO3hhRO-zSr-F-d5TlJcaJllI3QFKPdoEcMpxq5Xaf4=w720-h310\n\t")

        result = StringUtil.trim(app_item)

        self.__verify_trimmed(result)

    def test_trim_호출시__주어진_CategoryItem_내_모든_필드들에_트림을_적용한다(self):
        category_item = CategoryItem()

        category_item['id'] = '\n\t\r       \uFEFFGAME_ACTION                  '
        category_item['title'] = '  액션       \n  \n  \n  \uFEFF'

        result = StringUtil.trim(category_item)

        self.__verify_trimmed(result)
