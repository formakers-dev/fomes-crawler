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

        self.assertEqual('com.test.1', upserted_app_usages[0]['packageName'])
        self.assertEqual(100, upserted_app_usages[0]['totalUsedTime'])
        self.assertEqual('user1@test.io', upserted_app_usages[0]['userId'])
        self.assertEqual('테스트앱1 - 앱사용정보 업데이트', upserted_app_usages[0]['appName'])
        self.assertEqual('GAME_ACTION', upserted_app_usages[0]['categoryId'])
        self.assertEqual('액션', upserted_app_usages[0]['categoryName'])
        self.assertEqual('TEST 2 Studio', upserted_app_usages[0]['developer'])
        self.assertEqual('icon.test.com/2222', upserted_app_usages[0]['iconUrl'])

        self.assertEqual('com.test.1', upserted_app_usages[1]['packageName'])
        self.assertEqual(1000, upserted_app_usages[1]['totalUsedTime'])
        self.assertEqual('user2@test.io', upserted_app_usages[1]['userId'])
        self.assertEqual('테스트앱1 - 앱사용정보 업데이트', upserted_app_usages[1]['appName'])
        self.assertEqual('GAME_ACTION', upserted_app_usages[1]['categoryId'])
        self.assertEqual('액션', upserted_app_usages[1]['categoryName'])
        self.assertEqual('TEST 2 Studio', upserted_app_usages[1]['developer'])
        self.assertEqual('icon.test.com/2222', upserted_app_usages[1]['iconUrl'])

        self.assertEqual('com.test.2', upserted_app_usages[2]['packageName'])
        self.assertEqual(10000, upserted_app_usages[2]['totalUsedTime'])
        self.assertEqual('user1@test.io', upserted_app_usages[2]['userId'])
        self.assertEqual('테스트앱2', upserted_app_usages[2]['appName'])
        self.assertEqual('GAME_PUZZLE', upserted_app_usages[2]['categoryId'])
        self.assertEqual('퍼즐', upserted_app_usages[2]['categoryName'])
        self.assertEqual('TEST DEV 2', upserted_app_usages[2]['developer'])
        self.assertEqual('icon.test.com/2', upserted_app_usages[2]['iconUrl'])

        self.assertEqual('com.test.2', upserted_app_usages[3]['packageName'])
        self.assertEqual(100000, upserted_app_usages[3]['totalUsedTime'])
        self.assertEqual('user2@test.io', upserted_app_usages[3]['userId'])
        self.assertEqual('테스트앱2', upserted_app_usages[3]['appName'])
        self.assertEqual('GAME_PUZZLE', upserted_app_usages[3]['categoryId'])
        self.assertEqual('퍼즐', upserted_app_usages[3]['categoryName'])
        self.assertEqual('TEST DEV 2', upserted_app_usages[3]['developer'])
        self.assertEqual('icon.test.com/2', upserted_app_usages[3]['iconUrl'])


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

class AppInfoUpdateTestCase(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()

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

    def tearDown(self) -> None:
        super().tearDown()

        DBManager.get_db()['app-usages'].delete_many({})

    def test_get_package_names_to_update_info_호출시__현재_앱_사용정보가_있는_앱들의_packageName들을_모두_가져온다(self):
        package_names = [
            'com.test.1',
            'com.test.2',
        ]
        result = DBManager.get_package_names_to_update_info()

        self.assertEqual(package_names, result)