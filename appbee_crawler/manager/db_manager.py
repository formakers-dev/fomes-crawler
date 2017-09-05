# -*- coding: utf-8 -*-
import os
from pymongo import MongoClient

class DBManager(object):
    db = None
    connection = None

    @classmethod
    def get_db(cls, new=False):
        if new or not cls.connection:
            cls.connection = MongoClient(os.environ['MONGO_URL'])
        if new or not cls.db:
            cls.db = cls.connection.appbee
        return cls.db

    @classmethod
    def close(cls):
        cls.connection.close()

    @classmethod
    def select_uncrawled_apps(cls):
        db = cls.get_db()
        docs = db['uncrawled-apps'].find()
        return docs

    @classmethod
    def delete_uncrawled_app(cls, package_name):
        db = cls.get_db()
        db['uncrawled-apps'].delete_one({'packageName': package_name})

    @classmethod
    def upsert_apps(cls, item):
        db = cls.get_db()
        db['apps'].update({'packageName':item['packageName']}, dict(item), upsert=True)

    @classmethod
    def upsert_categories(cls, item):
        db = cls.get_db()
        db['categories'].update({'id':item['id']}, dict(item), upsert=True)

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
