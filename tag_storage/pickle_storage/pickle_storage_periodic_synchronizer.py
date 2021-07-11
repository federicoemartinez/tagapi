from __future__ import annotations
import asyncio
import dataclasses
import datetime
from dataclasses import field
from typing import Optional

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from tag_storage.pickle_storage.pickle_storage import PickledSetTagStorage
from tag_storage.pickle_storage.pickle_storage_synchronizer import PickledSetTagStorageSynchronizer, \
    PickledSetTagStorageSynchronizerConfiguration

@dataclasses.dataclass
class PickledSetTagStoragePeriodicSynchronizerConfiguration(PickledSetTagStorageSynchronizerConfiguration):
    interval: datetime.interval = field(default_factory=lambda: datetime.timedelta(seconds=1))

class PickledSetTagStoragePeriodicSynchronizer(PickledSetTagStorageSynchronizer):
    interval: datetime.timedelta
    store: Optional[PickledSetTagStorage]

    def __init__(self, config: PickledSetTagStoragePeriodicSynchronizerConfiguration):
        self.config = config
        self.interval = config.interval
        self.store = None
        loop = asyncio.get_event_loop()
        self.task = loop.create_task(self.__sync_loop())

    async def __sync_loop(self):
        while True:
            await self.__sync()
            await asyncio.sleep(self.interval.total_seconds())

    async def __sync(self):
        if self.store:
            await self.store.online_sync()

    def sync_store(self, store: PickledSetTagStorage):
        self.store = store

    async def close(self):
        self.task.cancel()
        await self.__sync()


