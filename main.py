import logging

from app.create_app import create_app
from tag_storage.base_storage.async_tag_storage import AsyncTagStorage
from tag_storage.pickle_storage.pickle_storage import PickledSetTagStorage, PickledSetTagStorageConfiguration

import os

from tag_storage.py2neo_storage.py2neo_storage import Py2NeoStorageConfig, Py2NeoStorage

dir_path = "/tmp"
try:
    #config = PickledSetTagStorageConfiguration(path=os.path.join(dir_path,'data/tags_db'))
    #tag_store: AsyncTagStorage = PickledSetTagStorage(config)
    config=Py2NeoStorageConfig(url="bolt://127.0.0.1:7687", username=None, password=None)
    tag_store = Py2NeoStorage(config)
except Exception as e:
    logging.getLogger('root').exception(e)
    raise e
app = create_app(tag_store)
