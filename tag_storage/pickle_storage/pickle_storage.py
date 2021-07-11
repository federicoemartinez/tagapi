from __future__ import annotations

import copy
import dataclasses
import os.path
import pickle
from typing import Collection, Optional

import aiofiles
import aiorwlock
from sortedcontainers import SortedSet

from tag_storage.base_storage.async_tag_storage import AsyncTagStorage
from tag_storage.base_storage.tag_storage import TagStorageException
from tag_storage.pickle_storage.pickle_db_data import PickleDbData
from tag_storage.pickle_storage.pickle_storage_synchronizer import PickledSetTagStorageSynchronizer
from tag_storage.pickle_storage.pickle_storage_periodic_synchronizer import PickledSetTagStoragePeriodicSynchronizer, \
    PickledSetTagStoragePeriodicSynchronizerConfiguration


@dataclasses.dataclass
class PickledSetTagStorageConfiguration:
    path: str
    overwrite: bool = False
    synchronizer:PickledSetTagStorageSynchronizer = dataclasses.field(default_factory=lambda: PickledSetTagStoragePeriodicSynchronizer(PickledSetTagStoragePeriodicSynchronizerConfiguration()))

class InvalidPickleDatabaseFile(TagStorageException):
    pass

class PickledSetTagStorage(AsyncTagStorage):
    db_path:str
    lock:aiorwlock.RWLock
    db_data:PickleDbData
    synchronizer:PickledSetTagStorageSynchronizer
    config:PickledSetTagStorageConfiguration
    dirty:bool

    def __init__(self, config:PickledSetTagStorageConfiguration):
        self.dirty=False
        self.config = config
        self.lock = aiorwlock.RWLock()
        self.db_path = config.path
        if config.overwrite or not os.path.exists(self.db_path):
            self.db_data = PickleDbData()
            with open(self.db_path, 'wb') as f:
                pickle.dump(self.db_data, f)
        else:
            self.__load_data()
        self.synchronizer = config.synchronizer
        self.synchronizer.sync_store(self)

    def __load_data(self):
        # This is insecure
        with open(self.db_path, 'rb') as f:
            try:
                db_data = pickle.load(f)
            except (pickle.UnpicklingError, TypeError) as e:
                raise InvalidPickleDatabaseFile(f"{self.db_path} is not a valid pickle db: {e}")


        # TODO: validate the data
        self.db_data = db_data

    async def get_tags(self, limit: int = 100, offset: int = 0) -> Collection[str]:
        async with self.lock.reader_lock:
            return list(self.db_data.tags.islice(offset, offset + limit))

    async def get_objects(self, limit: int = 100, offset: int = 0) -> Collection[str]:
        async with self.lock.reader_lock:
            return list(self.db_data.objects.islice(offset, offset + limit))

    async def get_tagged_objects(self, tag: str, limit: int = 100, offset: int = 0) -> Collection[str]:
        async with self.lock.reader_lock:
            return list(self.db_data.tags.get(tag, SortedSet()).islice(offset, offset + limit))

    async def get_object_tags(self, tagged_object: str, limit: int = 100, offset: int = 0) -> Collection[str]:
        async with self.lock.reader_lock:
            return list(self.db_data.objects.get(tagged_object, SortedSet()).islice(offset, offset + limit))

    async def tag(self, object_to_tag: str, tags: Collection[str]):
        async with self.lock.writer_lock:
            tags_set = self.db_data.objects.get(object_to_tag)
            if tags_set is None:
                tags_set = SortedSet()
                self.db_data.objects[object_to_tag] = tags_set
            tags_set.update(tags)
            for each in tags:
                tagged_objects = self.db_data.tags.get(each)
                if tagged_objects is None:
                    tagged_objects = SortedSet()
                    self.db_data.tags[each] = tagged_objects
                tagged_objects.add(object_to_tag)
            self.dirty=True

    async def remove_tag(self, tag_to_remove: str):
        async with self.lock.writer_lock:
            tagged_objects = self.db_data.tags.pop(tag_to_remove, None)
            if tagged_objects is not None:
                for each in tagged_objects:
                    tags_set = self.db_data.objects.get(each)
                    if tags_set is None:
                        continue
                    tags_set.remove(tag_to_remove)
            self.dirty = True

    async def remove_object(self, object_to_remove: str):
        async with self.lock.writer_lock:
            tags = self.db_data.objects.pop(object_to_remove, None)
            if tags is not None:
                for each in tags:
                    objects_set = self.db_data.tags.get(each)
                    if objects_set is None:
                        continue
                    objects_set.remove(object_to_remove)
            self.dirty = True

    async def untag(self, object_to_untag: str, tags: Collection[str]):
        async with self.lock.writer_lock:
            tags_set = self.db_data.objects.get(object_to_untag)
            if tags_set is None:
                return
            tags_set.difference_update(tags)
            for each in tags:
                tagged_objects = self.db_data.tags.get(each)
                if tagged_objects is None:
                    continue
                tagged_objects.remove(object_to_untag)
            self.dirty = True

    async def offline_sync(self):
        async with self.lock.reader_lock:
            if self.dirty:
                async with aiofiles.open(self.db_path, 'wb') as f:
                    s = pickle.dumps(self.db_data)
                    await f.write(s)
                self.dirty=False

    async def online_sync(self):
        async with self.lock.reader_lock:
            if self.dirty:
                snapshot = copy.deepcopy(self.db_data)
                self.dirty=False
            else:
                return
        async with aiofiles.open(self.db_path, 'wb') as f:
            s = pickle.dumps(snapshot)
            await f.write(s)

    async def close(self):
        await self.synchronizer.close()
