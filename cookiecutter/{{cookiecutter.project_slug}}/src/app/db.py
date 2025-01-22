from typing import TYPE_CHECKING

from mm_base1.db import BaseDB, DatabaseAny

from app.models import Data

if TYPE_CHECKING:
    from mm_mongo import MongoCollection


class DB(BaseDB):
    def __init__(self, database: DatabaseAny) -> None:
        super().__init__(database)
        self.data: MongoCollection[Data] = Data.init_collection(database)
