
import unittest

import py2neo
import pytest
from py2neo import Graph


from tag_storage.py2neo_storage.py2neo_storage import Py2NeoStorageConfig, Py2NeoStorage

def there_is_a_ongdb():
    try:
        Graph("bolt://127.0.0.1:7687", auth=(None, None)).delete_all()
    except py2neo.errors.ConnectionUnavailable:
        return False
    return True

@pytest.mark.skipif(not there_is_a_ongdb(), reason="This test needs a neo4j or ongdb server in 127.0.0.1:7687 without auth")
class Py2NeoTest(unittest.TestCase):

    def setUp(self) -> None:
        config = Py2NeoStorageConfig(url="bolt://127.0.0.1:7687", username=None, password=None)
        Graph(config.url, auth=(config.username, config.password)).delete_all()
        tag_store = Py2NeoStorage(config)
        self.tag_store = tag_store

    def tearDown(self) -> None:
        config = Py2NeoStorageConfig(url="bolt://127.0.0.1:7687", username=None, password=None)
        Graph(config.url, auth=(config.username, config.password)).delete_all()

    
    def test_create_one(self):
            assert self.tag_store.get_tags() == []
            assert self.tag_store.get_objects() == []
            self.tag_store.close()
    
    def test_add_objects(self):
        
        tags = ["tag1", "tag2"]
        one_object = "one_object"
        self.tag_store.tag(one_object,tags)
        assert self.tag_store.get_object_tags(one_object) == tags
        assert self.tag_store.get_object_tags(one_object, limit=1) == [tags[0]]
        assert self.tag_store.get_object_tags(one_object, limit=1, offset=1) == [tags[1]]
        assert self.tag_store.get_objects() == [one_object]
        assert self.tag_store.get_tags() == tags
        assert self.tag_store.get_tagged_objects(tags[0]) == [one_object]
        assert self.tag_store.get_tagged_objects(tags[1]) == [one_object]
        another_object = "another_object"
        self.tag_store.tag(another_object, [tags[0]])
        assert self.tag_store.get_object_tags(one_object) == tags
        assert self.tag_store.get_object_tags(one_object, limit=1) == [tags[0]]
        assert self.tag_store.get_object_tags(another_object, limit=1, offset=1) == []
        assert self.tag_store.get_objects() == [another_object, one_object]
        assert self.tag_store.get_tags() == tags
        assert self.tag_store.get_tagged_objects(tags[0]) == [another_object, one_object]
        assert self.tag_store.get_tagged_objects(tags[1]) == [one_object]
        self.tag_store.close()
            
    
    
    def test_tag_and_untag(self):
        tags = ["tag1", "tag2"]
        one_object = "one_object"
        self.tag_store.tag(one_object,tags)
        self.tag_store.untag(one_object, [tags[1]])
        assert self.tag_store.get_object_tags(one_object) == [tags[0]]
        assert self.tag_store.get_tags() == tags # Tags are not removed
        assert self.tag_store.get_tagged_objects(tags[0]) == [one_object]
        assert self.tag_store.get_tagged_objects(tags[1]) == []
        self.tag_store.remove_tag(tags[0])
        assert self.tag_store.get_tags() == [tags[1]]
        assert self.tag_store.get_tagged_objects(tags[0]) == []
        assert self.tag_store.get_tagged_objects(tags[1]) == []
        assert self.tag_store.get_object_tags(one_object) == []
        self.tag_store.remove_object(one_object)
        assert self.tag_store.get_objects() == []
        self.tag_store.tag(one_object, tags)
        self.tag_store.remove_object(one_object)
        assert self.tag_store.get_objects() == []
        assert self.tag_store.get_tags() == tags

        self.tag_store.remove_tag('fake tag') # must not fail
        self.tag_store.remove_object('fake object')  # must not fail
        self.tag_store.untag("fake object 2", ['fake tag 2']) # must not fail
        self.tag_store.close()
