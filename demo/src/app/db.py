from bson import ObjectId
from mm_base1.db import BaseDB, DatabaseAny
from mm_mongo import MongoCollection

from app.models import Data


class DB(BaseDB):
    def __init__(self, database: DatabaseAny) -> None:
        super().__init__(database)
        self.data: MongoCollection[ObjectId, Data] = MongoCollection(database, Data)
