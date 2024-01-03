from pymongo import MongoClient


class Storage:
    """Manages storage in database"""
    __client = None

    def __init__(self):
        pass

    def client(self):
        return self.__client

    def load(self, host: str, port: int):
        if host and port:
            self.__client = MongoClient(host=host, port=port)
        else:
            self.__client = MongoClient()
