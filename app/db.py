from mm_mongo import DatabaseAny, MongoCollection

from app.models import Data


class DB:
    def __init__(self, database: DatabaseAny):
        self.data: MongoCollection[Data] = Data.init_collection(database)
