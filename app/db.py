from bson import ObjectId
from mm_mongo import DatabaseAny, MongoCollection

from app.models import Data


class DB:
    def __init__(self, database: DatabaseAny) -> None:
        self.data: MongoCollection[ObjectId, Data] = MongoCollection(database, Data)
