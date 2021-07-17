from __future__ import annotations

from typing import Union, Optional

from pydantic import BaseSettings, BaseModel

from tag_storage.base_storage.tag_storage import TagStorage
from tag_storage.pickle_storage.pickle_storage import PickledSetTagStorageConfiguration, PickledSetTagStorage
from tag_storage.py2neo_storage.py2neo_storage import Py2NeoStorageConfig


class TagStorageSettings(BaseModel):

    def get_storage(self) -> TagStorage:
        raise NotImplementedError()


class PickleDbSettings(TagStorageSettings):
    pickledb_path: str

    def get_storage(self):
        config = PickledSetTagStorageConfiguration(path=self.pickledb_path)
        storage = PickledSetTagStorage(config)
        return storage


class Py2NeoSettings(TagStorageSettings):
    py2neo_url: str
    py2neo_username: Optional[str] = None
    py2neo_password: Optional[str] = None

    def get_storage(self):
        config = Py2NeoStorageConfig(url=self.py2neo_url, username=self.py2neo_username, password=self.py2neo_password)
        storage = PickledSetTagStorage(config)
        return storage


class SupportedStorageSettings(TagStorageSettings):
    __root__: Union[PickleDbSettings, Py2NeoSettings]

    def get_storage(self):
        return self.__root__.get_storage()


class Settings(BaseSettings):
    app_name: str = "TagApi"
    tag_storage_settings: SupportedStorageSettings
