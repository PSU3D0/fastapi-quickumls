import asyncio
import logging
from concurrent.futures import ProcessPoolExecutor
from contextlib import asynccontextmanager

from quickumls import QuickUMLS

logger = logging.getLogger(__name__)


def worker_init_umlspool(quickumls_fp: str):
    global matcher
    matcher = QuickUMLS(
        quickumls_fp=quickumls_fp,
    )

    logger.info("Initialized QuickUMLS matcher")


def match(text: str):
    return matcher.match(text, best_match=True, ignore_syntax=False)


class QuickUmlsProcessPool:
    def __init__(self, quickumls_fp: str, max_size: int):
        self.quickumls_fp = quickumls_fp
        self.max_size = max_size
        self.pool = ProcessPoolExecutor(
            max_workers=max_size,
            initializer=worker_init_umlspool,
            initargs=(self.quickumls_fp,),
        )

    def __del__(self):
        self.pool.shutdown()

    async def match(self, text: str):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.pool, match, text)
