import unittest
from appbee_crawler.spiders.category_spider import *
from appbee_crawler.test.fake_response import fake_response


class CategorySpiderTestCase(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.spider = CategorySpider()

    def test_parse_with_success_response(self):
        response = fake_response('./data/category_data.html')
        result = self.spider.parse(response)
        self.assertEqual(len(result), 61)

    def test_parse_with_empty_response(self):
        response = fake_response('./data/empty_data.html')
        result = self.spider.parse(response)
        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main()
