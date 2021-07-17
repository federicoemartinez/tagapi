from __future__ import annotations

import abc
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

    @abc.abstractmethod
    def __init__(self, config: PickledSetTagStorageSynchronizerConfiguration):
        raise NotImplementedError

    @abc.abstractmethod
    async def sync_store(self, store: PickledSetTagStorage):
        raise NotImplementedError

    @abc.abstractmethod
    async def close(self):
        raise NotImplementedError
