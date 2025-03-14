import random
from datetime import timedelta
from decimal import Decimal

from bson import ObjectId
from mm_mongo import MongoInsertManyResult, MongoInsertOneResult
from mm_std import Err, Ok, utc_now

from app.models import Data, DataStatus
from app.services.base import AppService, AppServiceParams


class DataService(AppService):
    def __init__(self, base_params: AppServiceParams) -> None:
        super().__init__(base_params)

    def generate_data(self) -> MongoInsertOneResult:
        status = random.choice(list(DataStatus))
        value = random.randint(0, 1_000_000)
        self.dlog("data_generated", {"status": status, "value": value, "large-data": "abc" * 100})
        self.send_telegram_message(f"a new data: {value}")

        return self.db.data.insert_one(Data(id=ObjectId(), status=status, value=value))

    def generate_many(self) -> MongoInsertManyResult:
        new_data_list = [
            Data(id=ObjectId(), status=random.choice(list(DataStatus)), value=random.randint(0, 1_000_000)) for _ in range(10)
        ]
        return self.db.data.insert_many(new_data_list)

    def test_typings(self) -> dict[str, object]:
        return {
            "a1": self.dconfig.telegram_chat_id + 1,
            "a2": self.dconfig.price + Decimal("2.32"),
            "a3": self.dvalue.last_checked_at + timedelta(days=1),
            "a4": self.dvalue.processed_block + 321,
            "a5": Ok(utc_now(), data=[1, 2, 3]),
            "a6": Err("bla bla bla", data=123),
        }
