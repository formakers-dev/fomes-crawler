import unittest

from appbee_crawler.spiders.app_spider import AppSpider
from appbee_crawler.test.fake_response import fake_response

class TestAppSpider(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.spider = AppSpider()

    def test_request_similar_apps(self):
        response = fake_response('./data/free_app_data.html')
        generator = self.spider.request_similar_apps(response)
        self.assertEqual(next(generator)._get_url(), 'https://play.google.com/store/apps/details?id=com.disney.moanaislandlife_goo')
        self.assertEqual(next(generator)._get_url(), 'https://play.google.com/store/apps/details?id=com.sparklingsociety.cityislandairport2')
        self.assertEqual(next(generator)._get_url(), 'https://play.google.com/store/apps/details?id=com.astragon.cs2014')
        next(generator)
        next(generator)
        next(generator)
        next(generator)
        next(generator)
        self.assertRaises(StopIteration, next, generator)

if __name__ == '__main__':
    unittest.main()
