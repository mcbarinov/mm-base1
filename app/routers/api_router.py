import time
from decimal import Decimal
from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, File, UploadFile
from mm_mongo import MongoInsertOneResult, mongo_query
from mm_std import Err, Ok, utc_now
from starlette.responses import PlainTextResponse

from app.app import App
from app.models import DataStatus


def init(app: App) -> APIRouter:
    router = APIRouter()

    @router.get("/data")
    def get_data_list(worker: str | None = None, status: DataStatus | None = None, limit: int = 100):
        return app.db.data.find(mongo_query(worker=worker, status=status), "-created_at", limit)

    @router.post("/data/upload")
    async def upload_file(file: Annotated[UploadFile, File()]):
        return await file.read()

    @router.post("/data/generate")
    def generate_data() -> MongoInsertOneResult:
        return app.data_service.generate_data()

    @router.get("/data/{pk}")
    def get_data(pk: ObjectId):
        return app.db.data.get_or_none(pk)

    @router.post("/data/{pk}/inc")
    def inc_data(pk: ObjectId, value: int | None = None):
        return app.db.data.update(pk, {"$inc": {"value": value or 1}})

    @router.delete("/data/{pk}")
    def delete_data(pk: ObjectId):
        return app.db.data.delete(pk)

    @router.get("/sleep/{seconds}")
    def sleep(seconds: int):
        app.logger.debug("sleep %s seconds called", seconds)
        time.sleep(seconds)
        return f"sleep {seconds} seconds"

    @router.get("/test")
    def test_all():
        return [
            Decimal("30.2"),
            ObjectId(),
            app.data_service.generate_many(),
            app.data_service.test_typings(),
            Ok("bla bla"),
            utc_now(),
            Ok(utc_now(), data="c1"),
            Ok(utc_now(), data="c2"),
            Err("zzz", data=2),
        ]

    @router.post("/test-post-plain-text", response_class=PlainTextResponse)
    def text_post_plain_text():
        return "a\nb\nc\n"

    @router.get("/exception")
    def exception():
        raise RuntimeError("test runtime exception")

    return router
