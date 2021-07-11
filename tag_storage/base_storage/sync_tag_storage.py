from typing import Collection

from tag_storage.base_storage.tag_storage import TagStorage


class SyncTagStorage(TagStorage):

    def get_tags(self, limit: int = 100, offset: int = 0) -> Collection[str]:
        raise NotImplementedError

    def get_objects(self, limit: int = 100, offset: int = 0) -> Collection[str]:
        raise NotImplementedError

    def get_tagged_objects(self, tag: str, limit: int = 100, offset: int = 0) -> Collection[str]:
        raise NotImplementedError

    def get_object_tags(self, tagged_object: str, limit: int = 100, offset: int = 0) -> Collection[str]:
        raise NotImplementedError

    def tag(self, object_to_tag: str, tags: Collection[str]):
        raise NotImplementedError

    def untag(self, object_to_untag: str, tags: Collection[str]):
        raise NotImplementedError

    def remove_object(self, object_to_remove: str):
        raise NotImplementedError

    def remove_tag(self, tag_to_remove: str):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError