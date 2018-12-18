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
                cls.connection = MongoClient(os.environ['RELEASE_MONGO_URL'])

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
        cls.connection.close()

    @classmethod
    def select_uncrawled_apps(cls):
        db = cls.get_db()
        docs = db['uncrawled-apps'].find({'errCode': {'$exists': False}})
        # docs = db['uncrawled-apps'].find()
        return docs

    @classmethod
    def update_uncrawled_apps(cls, package_name, error_code):
        print('### Update Uncrawled App ### ' + str(package_name) + ' ' + str(error_code))
        db = cls.get_db()

        db['uncrawled-apps'].update_one({'packageName': package_name}, {"$set": {'errCode': error_code}}, upsert=False)

    @classmethod
    def delete_uncrawled_app(cls, package_name):
        print('### Delete Uncrawled App ### ' + str(package_name))
        db = cls.get_db()
        db['uncrawled-apps'].delete_one({'packageName': package_name})

    @classmethod
    def upsert_apps(cls, item):
        print('### Upsert Apps ### ' + str(item['packageName']))
        db = cls.get_db()
        db['apps'].update({'packageName': item['packageName']}, dict(item), upsert=True)

    @classmethod
    def upsert_categories(cls, item):
        print('### Upsert Categories ### ' + str(item['id']))
        db = cls.get_db()
        db['categories'].update({'id': item['id']}, dict(item), upsert=True)

    @classmethod
    def upsert_non_game_apps(cls, item):
        print('### Upsert Non Game App ### ' + str(item['packageName']))
        db = cls.get_db()
        db['non-game-apps'].update({'packageName': item['packageName']}, dict(item), upsert=True)

    @classmethod
    def select_apps(cls, package_name):
        db = cls.get_db()
        docs = db['apps'].find({'packageName': package_name})
        return docs

    @classmethod
    def select_user_apps(cls):
        db = cls.get_db()
        docs = db['user-apps'].find()
        return docs
