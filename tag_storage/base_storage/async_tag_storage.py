from typing import Collection

from tag_storage.base_storage.tag_storage import TagStorage


class AsyncTagStorage(TagStorage):

    async def get_tags(self, limit: int = 100, offset: int = 0) -> Collection[str]:
        raise NotImplementedError

    async def get_objects(self, limit: int = 100, offset: int = 0) -> Collection[str]:
        raise NotImplementedError

    async def get_tagged_objects(self, tag: str, limit: int = 100, offset: int = 0) -> Collection[str]:
        raise NotImplementedError

    async def get_object_tags(self, tagged_object: str, limit: int = 100, offset: int = 0) -> Collection[str]:
        raise NotImplementedError

    async def tag(self, object_to_tag: str, tags: Collection[str]):
        raise NotImplementedError

    async def untag(self, object_to_untag: str, tags: Collection[str]):
        raise NotImplementedError

    async def remove_object(self, object_to_remove: str):
        raise NotImplementedError

    async def remove_tag(self, tag_to_remove: str):
        raise NotImplementedError

    async def close(self):
        raise NotImplementedError
