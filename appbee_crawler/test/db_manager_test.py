import unittest

from appbee_crawler.manager.db_manager import DBManager


class UpsertAppsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        app_usages = [
            {
                'userId': 'user1@test.io',
                'totalUsedTime': 100,
                'packageName': 'com.test.1',
                'appName': '테스트앱1',
                'categoryId': 'GAME_PUZZLE',
                'categoryName': '퍼즐',
                'developer': 'TEST DEV 1',
                'iconUrl': 'icon.test.com/1'
            },
            {
                'userId': 'user2@test.io',
                'totalUsedTime': 1000,
                'packageName': 'com.test.1',
                'appName': '테스트앱1',
                'categoryId': 'GAME_PUZZLE',
                'categoryName': '퍼즐',
                'developer': 'TEST DEV 1',
                'iconUrl': 'icon.test.com/1'
            },
            {
                'userId': 'user1@test.io',
                'totalUsedTime': 10000,
                'packageName': 'com.test.2',
                'appName': '테스트앱2',
                'categoryId': 'GAME_PUZZLE',
                'categoryName': '퍼즐',
                'developer': 'TEST DEV 2',
                'iconUrl': 'icon.test.com/2'
            },
            {
                'userId': 'user2@test.io',
                'totalUsedTime': 100000,
                'packageName': 'com.test.2',
                'appName': '테스트앱2',
                'categoryId': 'GAME_PUZZLE',
                'categoryName': '퍼즐',
                'developer': 'TEST DEV 2',
                'iconUrl': 'icon.test.com/2'
            },
        ]

        DBManager.get_db()['app-usages'].insert_many(app_usages)

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

        DBManager.get_db()['app-usages'].delete_many({})

    def setUp(self):
        super().setUp()

        apps = [
            {
                'packageName': 'com.test.1',
                'appName': '테스트앱1',
                'categoryId1': 'GAME_PUZZLE',
                'categoryName1': '퍼즐',
                'developer': 'TEST DEV 1',
                'iconUrl': 'icon.test.com/1'
            },
            {
                'packageName': 'com.test.2',
                'appName': '테스트앱2',
                'categoryId1': 'GAME_PUZZLE',
                'categoryName1': '퍼즐',
                'developer': 'TEST DEV 2',
                'iconUrl': 'icon.test.com/2'
            },
        ]

        DBManager.get_db()['apps'].insert_many(apps)

    def tearDown(self):
        super().tearDown()

        DBManager.get_db()['apps'].delete_many({})

    def test_upsert_apps_호출시__apps_컬렉션에_이미_앱정보가_존재하는_경우__해당_앱정보를_업데이트한다(self):
        apps = [
            {
                'packageName': 'com.test.1',
                'appName': '테스트앱1 - 이벤트',
                'categoryId1': 'GAME_PUZZLE',
                'categoryName1': '퍼즐',
                'developer': 'TEST DEV 1',
                'iconUrl': 'icon.test.com/1'
            }
        ]

        for app in apps:
            DBManager.upsert_app(app)

        upserted_apps = DBManager.get_db()['apps'].find({'packageName': 'com.test.1'})

        upserted_apps.sort('packageName')

        self.assertEqual(upserted_apps[0]['packageName'], 'com.test.1')
        self.assertEqual(upserted_apps[0]['appName'], '테스트앱1 - 이벤트')
        self.assertEqual(upserted_apps[0]['categoryId1'], 'GAME_PUZZLE')
        self.assertEqual(upserted_apps[0]['categoryName1'], '퍼즐')
        self.assertEqual(upserted_apps[0]['developer'], 'TEST DEV 1')
        self.assertEqual(upserted_apps[0]['iconUrl'], 'icon.test.com/1')

    def test_upsert_apps_호출시__apps_컬렉션에_이미_앱정보가_없는_경우__해당_앱정보를_추가한다(self):
        apps = [
            {
                'packageName': 'com.test.3',
                'appName': '테스트앱3',
                'categoryId1': 'GAME_ACTION',
                'categoryName1': '액션',
                'developer': 'TEST DEV 3',
                'iconUrl': 'icon.test.com/3'
            }
        ]

        for app in apps:
            DBManager.upsert_app(app)

        upserted_apps = DBManager.get_db()['apps'].find({'packageName': 'com.test.3'})

        upserted_apps.sort('packageName')

        self.assertEqual(upserted_apps[0]['packageName'], 'com.test.3')
        self.assertEqual(upserted_apps[0]['appName'], '테스트앱3')
        self.assertEqual(upserted_apps[0]['categoryId1'], 'GAME_ACTION')
        self.assertEqual(upserted_apps[0]['categoryName1'], '액션')
        self.assertEqual(upserted_apps[0]['developer'], 'TEST DEV 3')
        self.assertEqual(upserted_apps[0]['iconUrl'], 'icon.test.com/3')

    def test_upsert_apps_호출시__갱신되는_앱의_사용정보가_있을_경우__해당_앱사용정보들을_업데이트한다(self):

        apps = [
            {
                'packageName': 'com.test.1',
                'appName': '테스트앱1 - 앱사용정보 업데이트',
                'categoryId1': 'GAME_ACTION',
                'categoryName1': '액션',
                'developer': 'TEST 2 Studio',
                'iconUrl': 'icon.test.com/2222'
            }
        ]

        for app in apps:
            DBManager.upsert_app(app)

        upserted_app_usages = DBManager.get_db()['app-usages'].find({})

        upserted_app_usages.sort('totalUsedTime')

        self.assertEqual(upserted_app_usages[0]['packageName'], 'com.test.1')
        self.assertEqual(upserted_app_usages[0]['totalUsedTime'], 100)
        self.assertEqual(upserted_app_usages[0]['userId'], 'user1@test.io')
        self.assertEqual(upserted_app_usages[0]['appName'], '테스트앱1 - 앱사용정보 업데이트')
        self.assertEqual(upserted_app_usages[0]['categoryId'], 'GAME_ACTION')
        self.assertEqual(upserted_app_usages[0]['categoryName'], '액션')
        self.assertEqual(upserted_app_usages[0]['developer'], 'TEST 2 Studio')
        self.assertEqual(upserted_app_usages[0]['iconUrl'], 'icon.test.com/2222')

        self.assertEqual(upserted_app_usages[1]['packageName'], 'com.test.1')
        self.assertEqual(upserted_app_usages[1]['totalUsedTime'], 1000)
        self.assertEqual(upserted_app_usages[1]['userId'], 'user2@test.io')
        self.assertEqual(upserted_app_usages[1]['appName'], '테스트앱1 - 앱사용정보 업데이트')
        self.assertEqual(upserted_app_usages[1]['categoryId'], 'GAME_ACTION')
        self.assertEqual(upserted_app_usages[1]['categoryName'], '액션')
        self.assertEqual(upserted_app_usages[1]['developer'], 'TEST 2 Studio')
        self.assertEqual(upserted_app_usages[1]['iconUrl'], 'icon.test.com/2222')

        self.assertEqual(upserted_app_usages[2]['packageName'], 'com.test.2')
        self.assertEqual(upserted_app_usages[2]['totalUsedTime'], 10000)
        self.assertEqual(upserted_app_usages[2]['userId'], 'user1@test.io')
        self.assertEqual(upserted_app_usages[2]['appName'], '테스트앱2')
        self.assertEqual(upserted_app_usages[2]['categoryId'], 'GAME_PUZZLE')
        self.assertEqual(upserted_app_usages[2]['categoryName'], '퍼즐')
        self.assertEqual(upserted_app_usages[2]['developer'], 'TEST DEV 2')
        self.assertEqual(upserted_app_usages[2]['iconUrl'], 'icon.test.com/2')

        self.assertEqual(upserted_app_usages[3]['packageName'], 'com.test.2')
        self.assertEqual(upserted_app_usages[3]['totalUsedTime'], 100000)
        self.assertEqual(upserted_app_usages[3]['userId'], 'user2@test.io')
        self.assertEqual(upserted_app_usages[3]['appName'], '테스트앱2')
        self.assertEqual(upserted_app_usages[3]['categoryId'], 'GAME_PUZZLE')
        self.assertEqual(upserted_app_usages[3]['categoryName'], '퍼즐')
        self.assertEqual(upserted_app_usages[3]['developer'], 'TEST DEV 2')
        self.assertEqual(upserted_app_usages[3]['iconUrl'], 'icon.test.com/2')


class UncrawledAppTestCase(unittest.TestCase):

    def setUp(self):
        super().setUp()

        uncrawled_apps = [
            {
                'packageName': 'test.uncrawled.0',
                'errCode': 404
            },
            {
                'packageName': 'test.uncrawled.1',
            }
        ]

        DBManager.get_db()['uncrawled-apps'].insert_many(uncrawled_apps)

    def tearDown(self):
        super().tearDown()

        DBManager.get_db()['uncrawled-apps'].delete_many({})

    def test_get_uncrawled_apps_without_error_code_호출시__에러코드가_없는_언크롤드앱정보를_모두_가져온다(self):
        uncrawled_app_count = DBManager.get_db()['uncrawled-apps'].count_documents({'errCode': {'$exists': False}})
        uncrawled_apps = DBManager.get_db()['uncrawled-apps'].find({'errCode': {'$exists': False}})

        self.assertEqual(1, uncrawled_app_count)
        self.assertEqual('test.uncrawled.1', uncrawled_apps[0]['packageName'])

    def test_delete_uncrawled_app_호출시__입력한_packageName에_해당하는_언크롤드앱_정보를_삭제한다(self):
        DBManager.delete_uncrawled_app('test.uncrawled.1')
        uncrawled_app_count = DBManager.get_db()['uncrawled-apps'].count_documents({'errCode': {'$exists': False}})

        self.assertEqual(0, uncrawled_app_count)
