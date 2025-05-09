import string
from abc import ABC, abstractmethod
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from utils.utils import mongo_config

# Interface of db class


class DBConnection(ABC):
    @abstractmethod
    def insert_data(self):
        pass

    @abstractmethod
    def check_existence(self):
        pass


class MongoDB(DBConnection):

    _instance = None
    _initialised = False
    db_config = mongo_config()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self,  client: str = db_config['client'], db: str = db_config['db'], collection: str = db_config['collection']):
        try:
            if not self.__class__._initialised:
                self.client = MongoClient(client)
                self.db = self.client[db]
                self.collection = self.db[collection]
                self.__class__._initialised = True
            else:
                return
        except ConnectionFailure as ex:
            raise ConnectionError("MongoDB connection failed") from ex
        except Exception as ex:
            raise RuntimeError(
                f"Failed to initialize MongoDB client: {ex}") from ex

    def insert_data(self, data: dict):
        try:
            response = self.collection.insert_one(data)
            return response.inserted_id
        except Exception as ex:
            raise RuntimeError(f"Failed to insert data: {ex}") from ex

    def check_existence(self, link):
        try:
            exist = self.collection.find_one({'short_link': link})
            return exist
        except Exception as ex:
            raise Exception(f"Error: {ex}") from ex


class Compressor:

    BASE62_CHARS = string.digits + \
        string.ascii_lowercase + string.ascii_uppercase

    def __init__(self, input_string: str):
        self.string = input_string

    @classmethod
    def int_to_base62(cls, num):
        if num == 0:
            return cls.BASE62_CHARS[0]

        base62 = ""
        while num > 0:
            num, rem = divmod(num, 62)
            base62 = cls.BASE62_CHARS[rem] + base62
        return base62

    def string_to_base62(self):
        # Convert string to bytes, then to integer
        num = int.from_bytes(self.string.encode('utf-8'), 'big')
        return self.int_to_base62(num)[:8]


class LinkShortner:

    def __init__(self, long_link, db: MongoDB = MongoDB):
        self.long_link = long_link
        self.conn = db
        self.short_link = None

    def generate_unique_short_link(self):
        attempt = 0
        max_attempts = 5

        while attempt < max_attempts:
            compressor = Compressor(self.long_link + str(attempt))
            short_link = compressor.string_to_base62()
            existing = self.conn.check_existence(short_link)
            if not existing:
                return short_link
            elif existing['long_link'] == self.long_link:
                return short_link
            attempt += 1
        raise Exception(
            "Unable to generate unique short link after multiple attempts.")

    def deploy_short_link(self):
        try:
            short_link = self.generate_unique_short_link()
            now = datetime.now()
            data = {
                "short_link": short_link,
                "long_link": self.long_link,
                "created_at": now,
            }
            self.conn.insert_data(data)
            return short_link
        except Exception as ex:
            return ex


def get_long_link(link):
    try:
        conn = MongoDB()
        exist = conn.check_existence(link)
        if exist:
            long_url = exist.get("long_link")
            return long_url
    except ConnectionError as ex:
        return ex
    except Exception as ex:
        return ex
