import unittest
from appbee_crawler.util.string_util import StringUtil


class StringUtilTest(unittest.TestCase):

    def test_parse_number(self):
        self.assertEqual(StringUtil.parseNumber("100,000"), 100000)
        self.assertEqual(StringUtil.parseNumber(" 111,222,333 "), 111222333)