import redis
import json
import os


class Cache(object):

    def __init__(self,host:str='localhost',password:str=None):
        if host == 'localhost':
            print('localstorage enabled')

            self.disk = True
            self.storagePath = "cache/data"
            self.db = None
        elif password:
            print(f'redis cache enabled, password on')
            REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
            REDIS_PORT = os.getenv("REDIS_PORT", "6379")

            self.disk = False
            self.db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, errors='strict', password=password)
        else:
            print('redis cache enabled')
            REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
            REDIS_PORT = os.getenv("REDIS_PORT", "6379")

            self.disk = False
            self.db = redis.Redis(host=REDIS_HOST,port=REDIS_PORT)

    def read(self, key):
        if self.disk and not os.path.exists(self.storagePath):
            os.makedirs(self.storagePath)

        if os.path.exists(f'{self.storagePath}/{key}.json'):
            print(f'reading data from disk as {key}, storage={self.storagePath}/{key}.json')
            with open(f'{self.storagePath}/{key}.json','r') as f:
                data = json.load(f)
                f.close()
            return data
        else:
            return None


    def write(self, key, data):
        if self.disk and not os.path.exists(self.storagePath):
            os.makedirs(self.storagePath)

        with open(f'{self.storagePath}/{key}.json', 'w') as f:
            print(f'writing data to disk as {key}, storage={self.storagePath}/{key}.json')
            json.dump(data, f)
            f.close()

        return True