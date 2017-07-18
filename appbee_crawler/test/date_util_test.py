import unittest
from appbee_crawler.util.date_util import DateUtil

class DateUtilTest(unittest.TestCase):

    def test_get_date_format(self):
        self.assertEqual(DateUtil.get_date_format("2017년 7월 15일"), "20170715")
        self.assertEqual(DateUtil.get_date_format("2017년7월15일"), "20170715")
