import os
import json

from common.path import CACHE_PATH


class CoreCache(object):
    __data = dict()

    def __init__(self):
        self.load_cache_in_json()

    def load_cache_in_json(self):
        if os.path.isfile(CACHE_PATH):
            self.__data = json.load(open(CACHE_PATH, encoding='utf-8'))

    def sync_to_file(self):
        json.dump(self.__data, open(CACHE_PATH, 'w'), indent=4)

    def get_from_cache(self, key):
        return self.__data.get(key)

    def set_to_cache(self, key, value):
        self.__data.update({key: value})
        self.sync_to_file()


g_cache = CoreCache()
