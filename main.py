import logging

from app.create_app import create_app
from tag_storage.base_storage.async_tag_storage import AsyncTagStorage
from tag_storage.pickle_storage.pickle_storage import PickledSetTagStorage, PickledSetTagStorageConfiguration

import os
dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    config = PickledSetTagStorageConfiguration(path=os.path.join(dir_path,'data/tags_db'))
    tag_store: AsyncTagStorage = PickledSetTagStorage(config)
except Exception as e:
    logging.getLogger('root').exception(e)
    raise e
app = create_app(tag_store)
