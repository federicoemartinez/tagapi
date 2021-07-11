from __future__ import annotations

import dataclasses
from abc import ABC

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from tag_storage.pickle_storage.pickle_storage import PickledSetTagStorage

@dataclasses.dataclass
class PickledSetTagStorageSynchronizerConfiguration:
    pass

class PickledSetTagStorageSynchronizer(ABC):
    """
     # Takes responsibility of synchronize the store based on different strategies

    #Parameters:
    #    store (PickledSetTagStorage): The store to sync

    """

    def __init__(self, config:PickledSetTagStorageSynchronizerConfiguration):
        raise NotImplementedError

    async def sync_store(self, store: PickledSetTagStorage):
        raise NotImplementedError

    async def close(self):
        raise NotImplementedError


