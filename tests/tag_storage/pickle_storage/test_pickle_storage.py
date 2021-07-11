import os.path
import pickle
import tempfile
import unittest

import pytest

from tag_storage.pickle_storage.pickle_db_data import PickleDbData
from tag_storage.pickle_storage.pickle_storage import PickledSetTagStorage, PickledSetTagStorageConfiguration


@pytest.mark.asyncio
async def test_create_one():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, 'test')
        config = PickledSetTagStorageConfiguration(path=file_path)
        storage = PickledSetTagStorage(config)
        assert os.path.isfile(file_path)
        assert await storage.get_tags() == []
        assert await storage.get_objects() == []
        await storage.close()
        with open(file_path,'rb') as db_file:
            data = pickle.load(db_file)
            assert isinstance(data, PickleDbData)

@pytest.mark.asyncio
async def test_add_objects():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, 'test')
        config = PickledSetTagStorageConfiguration(path=file_path)
        storage = PickledSetTagStorage(config)
        tags = ["tag1", "tag2"]
        one_object = "one_object"
        await storage.tag(one_object,tags)
        assert await storage.get_object_tags(one_object) == tags
        assert await storage.get_object_tags(one_object, limit=1) == [tags[0]]
        assert await storage.get_object_tags(one_object, limit=1, offset=1) == [tags[1]]
        assert await storage.get_objects() == [one_object]
        assert await storage.get_tags() == tags
        assert await storage.get_tagged_objects(tags[0]) == [one_object]
        assert await storage.get_tagged_objects(tags[1]) == [one_object]
        another_object = "another_object"
        await storage.tag(another_object, [tags[0]])
        assert await storage.get_object_tags(one_object) == tags
        assert await storage.get_object_tags(one_object, limit=1) == [tags[0]]
        assert await storage.get_object_tags(another_object, limit=1, offset=1) == []
        assert await storage.get_objects() == [another_object, one_object]
        assert await storage.get_tags() == tags
        assert await storage.get_tagged_objects(tags[0]) == [another_object, one_object]
        assert await storage.get_tagged_objects(tags[1]) == [one_object]
        await storage.close()
        


