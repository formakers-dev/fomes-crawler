# -*- coding: utf-8 -*-
import os

from pymongo import MongoClient


class DBManager(object):
    db = None
    connection = None

    @classmethod
    def get_db(cls):
        if not cls.db:
            if not cls.connection:
                cls.connection = MongoClient(os.environ['CRAWLER_MONGO_URL'])

            if os.environ['PYTHON_ENV'] in ['development', 'staging', 'production']:
                cls.db = cls.connection.appbee
                print('Use appbee db for', os.environ['PYTHON_ENV'], 'environment')
            elif os.environ['PYTHON_ENV'] in ['test']:
                cls.db = cls.connection.test
                print('Use test db for', os.environ['PYTHON_ENV'], 'environment')
            else:
                print('Wrong environment:', os.environ['PYTHON_ENV'])

        return cls.db

    @classmethod
    def close(cls):
        if cls.connection:
            cls.connection.close()

    @classmethod
    def get_uncrawled_package_names_without_error_code(cls):
        db = cls.get_db()
        uncrawled_package_names = db['uncrawled-apps'].distinct('packageName', {'errCode': {'$exists': False}})
        other_apps_package_names = db['other-apps'].distinct('packageName')

        return list(filter(lambda package_name: package_name not in other_apps_package_names, uncrawled_package_names))

    @classmethod
    def update_error_code_of_uncrawled_app(cls, package_name, error_code):
        print('### Update errCode:' + str(error_code) + ' of ' + str(package_name) + 'in Uncrawled Apps ###')
        db = cls.get_db()

        db['uncrawled-apps'].update_one({'packageName': package_name}, {"$set": {'errCode': error_code}}, upsert=False)

    @classmethod
    def delete_uncrawled_app(cls, package_name):
        print('### Delete ' + str(package_name) + ' from Uncrawled Apps ###')
        db = cls.get_db()
        db['uncrawled-apps'].delete_one({'packageName': package_name})

    @classmethod
    def update_app_usages(cls, item):
        app_info = {
            'appName': item['appName'],
            'categoryId': item['categoryId1'],
            'categoryName': item['categoryName1'],
            'developer': item['developer'],
            'iconUrl': item['iconUrl'],
        }

        DBManager.get_db()['app-usages'].update_many({'packageName': item['packageName']}, {'$set': app_info})

    @classmethod
    def upsert_app(cls, item):
        print('### Upsert ' + str(item['packageName']) + ' to Apps ###')
        db = cls.get_db()
        db['apps'].update_one({'packageName': item['packageName']}, {'$set': dict(item)}, upsert=True)
        cls.update_app_usages(item)

    @classmethod
    def upsert_category(cls, item):
        print('### Upsert ' + str(item['id']) + ' to Categories ###')
        db = cls.get_db()
        db['categories'].update_one({'id': item['id']}, {'$set': dict(item)}, upsert=True)

    @classmethod
    def upsert_other_app(cls, item):
        print('### Upsert ' + str(item['packageName']) + ' to Other App ###')
        db = cls.get_db()
        db['other-apps'].update_one({'packageName': item['packageName']}, {'$set': dict(item)}, upsert=True)

    @classmethod
    def get_package_names_to_update_info(cls):
        db = cls.get_db()
        package_names = db['app-usages'].distinct('packageName')
        return package_names
