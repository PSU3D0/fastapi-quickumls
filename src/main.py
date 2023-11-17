import logging
import multiprocessing
import os

from fastapi import FastAPI
from pydantic import BaseModel, Field

from pool import QuickUmlsProcessPool

logger = logging.getLogger(__name__)

quickumls_pool = None


def on_startup():
    global quickumls_pool

    logger.info("Initializing QuickUMLS process pool")
    quickumls_pool = QuickUmlsProcessPool(
        quickumls_fp="/app/umls", max_size=multiprocessing.cpu_count()
    )


def on_shutdown():
    global quickumls_pool
    if quickumls_pool:
        quickumls_pool.pool.shutdown()


app = FastAPI(
    title="QuickUMLS API",
    description="A simple API for the QuickUMLS library",
    version="0.1.0",
    on_startup=[on_startup],
    on_shutdown=[on_shutdown],
)

MAX_CONCURRENCY = os.environ.get("FASTAPI_UMLS_WORKER_CONCURRENCY") or min(
    multiprocessing.cpu_count() - 2, 2
)


class MatchRequest(BaseModel):
    text: str = Field(
        ...,
        example="Patient has a history of diabetes mellitus type 2.",
        max_length=1000,
    )


@app.get("/match")
async def match(item: MatchRequest):
    result = await quickumls_pool.match(item.text)

    return result
