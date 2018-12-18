import re
import unittest

from appbee_crawler.app_items import AppItem
from appbee_crawler.category_items import CategoryItem
from appbee_crawler.util.string_util import StringUtil


class StringUtilTest(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.app_item = AppItem()
        self.category_item = CategoryItem()
        self.trimmedPattern = re.compile('(^[\s\uFEFF]+|[\s\uFEFF]+$)')

    def test_parse_number(self):
        self.assertEqual(StringUtil.parseNumber("100,000"), 100000)
        self.assertEqual(StringUtil.parseNumber(" 111,222,333 "), 111222333)

    def __check_not_trimmed(self, obj):
        not_trimmed_count = 0

        if type(obj) is str:
            if self.trimmedPattern.match(obj):
                print(obj, 'is not trimmed')
                not_trimmed_count += 1
        elif type(obj) is list:
            for item in obj:
                not_trimmed_count += self.__check_not_trimmed(item)
        elif type(obj) is dict:
            for value in obj.values():
                not_trimmed_count += self.__check_not_trimmed(value)
        elif type(obj) is AppItem:
            for value in obj.values():
                not_trimmed_count += self.__check_not_trimmed(value)

        return not_trimmed_count

    def test_trim_with_app_item(self):
        self.app_item['appName'] = ' 마이 오아시스 - 힐링되는 하늘섬 키우기                   \t \t \t '
        self.app_item['packageName'] = '\n\t         com.buffstudio.myoasis '
        self.app_item['appPrice'] = 0
        self.app_item['categoryId1'] = 'GAME_SIMULATION\n'
        self.app_item['categoryName1'] = '시뮬레이션'
        self.app_item['categoryId2'] = ' FAMILY_ACTION    \uFEFF \uFEFF \uFEFF'
        self.app_item['categoryName2'] = '\n액션/어드벤처 '
        self.app_item['contentsRating'] = '\n만 3세 이상 '
        self.app_item['description'] = '\uFEFF탭해서 하트를 모아 다양한 동물들이 뛰노는 오아시스'
        self.app_item['developer'] = '  Buff Studio Co.Ltd.             \uFEFF\t\t'
        self.app_item['star'] = 4.649204254150391
        self.app_item['installsMin'] = 1000000
        self.app_item['installsMax'] = 5000000
        self.app_item['reviewCount'] = 99833
        self.app_item['updatedDate'] = "20180629    "
        self.app_item['inappPriceMin'] = 1100
        self.app_item['inappPriceMax'] = 110000
        self.app_item['similarApps'] = list()
        self.app_item['similarApps'] = []
        self.app_item['similarApps'].append("  com.idleif.abyssrium\t")
        self.app_item['similarApps'].append("\ncom.idleif.abyssrium\t")
        self.app_item['similarApps'].append("      com.idleif.abyssrium")
        self.app_item['iconUrl'] = "\t\t\t          https://lh3.googleusercontent.com/OJ12eDDC6zShVguWb2mBS--cdUDRy4BzyqR_BfTy8kG5ibNwsbYbibNUnEW-hxUMlUM=s180\n\n\n"

        self.app_item['imageUrls'] = []
        self.app_item['imageUrls'].append("https://lh3.googleusercontent.com/TVyiUM_oGq1IRvMWdQNA-mr8Vl4WdkEqdiObLfYadyyF9OoTHSZT8AnsvYFFxffkTw=w720-h310\uFEFF")
        self.app_item['imageUrls'].append("\uFEFF  https://lh3.googleusercontent.com/JWAY26HZZwFGW5LwgGJaqYe5CXGePh_oLNPtRwNGZnLpa8n-MDnVeEGs0y9ALAMyNv4=w720-h310  ")
        self.app_item['imageUrls'].append("\t\uFEFF\t\t     https://lh3.googleusercontent.com/voBPYesTu9PKPvOo8VKQc15YLO3hhRO-zSr-F-d5TlJcaJllI3QFKPdoEcMpxq5Xaf4=w720-h310\n\t")

        self.app_item = StringUtil.trim(self.app_item)

        not_trimmed_count = self.__check_not_trimmed(self.app_item)

        self.assertEqual(not_trimmed_count, 0)

    def test_trim_with_category_item(self):
        self.category_item['id'] = '\n\t\r       \uFEFFGAME_ACTION                  '
        self.category_item['title'] = '  액션       \n  \n  \n  \uFEFF'

        self.category_item = StringUtil.trim(self.category_item)

        not_trimmed_count = self.__check_not_trimmed(self.category_item)

        self.assertEqual(not_trimmed_count, 0)