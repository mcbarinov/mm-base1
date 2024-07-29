from mm_base1.db import DatabaseAny
from mm_mongo import MongoCollection

from app.models import Data


class DB:
    def __init__(self, database: DatabaseAny):
        self.data: MongoCollection[Data] = Data.init_collection(database)
