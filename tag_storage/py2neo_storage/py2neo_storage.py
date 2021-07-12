import dataclasses
from typing import Collection

from py2neo import Graph, NodeMatcher, Node, Relationship, RelationshipMatcher, IN

from tag_storage.base_storage.sync_tag_storage import SyncTagStorage

@dataclasses.dataclass
class Py2NeoStorageConfig:
    url:str
    username:str
    password:str


class Py2NeoStorage(SyncTagStorage):

    TAG = 'tag'
    OBJECT ='object'
    TAGGED = 'Tagged'

    def __init__(self, config:Py2NeoStorageConfig):
        self.config = config
        self.graph = Graph(config.url, auth=(config.username, config.password))

    def get_tags(self, limit: int = 100, offset: int = 0) -> Collection[str]:
        nodes = NodeMatcher(self.graph)
        match = nodes.match(self.TAG).order_by("_.name").limit(limit).skip(offset)
        return [x['name'] for x in match]

    def get_objects(self, limit: int = 100, offset: int = 0) -> Collection[str]:
        nodes = NodeMatcher(self.graph)
        match = nodes.match(self.OBJECT).order_by("_.name").limit(limit).skip(offset).all()
        return [x['name'] for x in match]

    def get_tagged_objects(self, tag: str, limit: int = 100, offset: int = 0) -> Collection[str]:
        res = self.graph.run("MATCH p=(a)-[:%s]->(:%s {name:$name }) RETURN a.name order by a.name skip %d limit %d" % (self.TAGGED, self.TAG, offset, limit), {'name':tag} )
        return [x[0] for x in res]

    def get_object_tags(self, tagged_object: str, limit: int = 100, offset: int = 0) -> Collection[str]:
        res = self.graph.run("MATCH p=(:%s {name:$name })-[:%s]->(a) RETURN a.name order by a.name skip %d limit %d" % (
        self.OBJECT, self.TAGGED, offset, limit), {'name': tagged_object})
        return [x[0] for x in res]

    def tag(self, object_to_tag: str, tags: Collection[str]):
        nodes = NodeMatcher(self.graph)
        object_node = nodes.match(self.OBJECT, name=object_to_tag).first()
        if object_node is None:
            object_node= self.__create_object(object_to_tag)
        existing_tags = {n['name']:n for n in nodes.match(self.TAG, name=IN(tags)).all()}
        existing_edges = set()
        for tag_name, tag_node in existing_tags.items():
            edge = RelationshipMatcher(self.graph).match(nodes=(object_node,tag_node),r_type=self.TAGGED).first()
            if edge is not None:
                existing_edges.add(tag_name)

        for each in tags:
            if each not in existing_tags:
                existing_tags[each] = self.__create_tag(each)
        tx = self.graph.begin()
        for tag_name, tag_node in existing_tags.items():
            if tag_name not in existing_edges:
                rel = Relationship(object_node, self.TAGGED, tag_node)
                tx.create(rel)
        self.graph.commit(tx)
        


    def __create_tag(self, tag_name):
        n = Node(self.TAG, name=tag_name)
        self.graph.create(n)
        return n

    def __create_object(self, object_name):
        n = Node(self.OBJECT, name=object_name)
        self.graph.create(n)
        return n

    def untag(self, object_to_untag: str, tags: Collection[str]):
        nodes = NodeMatcher(self.graph)
        object_node = nodes.match(self.OBJECT, name=object_to_untag).first()
        if object_node is None:
            return
        existing_tags = {n['name']: n for n in nodes.match(self.TAG, name=IN(tags)).all()}
        existing_edges = []
        for tag_name, tag_node in existing_tags.items():
            edge = RelationshipMatcher(self.graph).match(nodes=(object_node,tag_node),r_type=self.TAGGED).first()
            if edge is not None:
                existing_edges.append(edge)
        tx = self.graph.begin()
        for each in existing_edges:
            tx.separate(each)
        self.graph.commit(tx)

    def remove_object(self, object_to_remove: str):
        object_node = NodeMatcher(self.graph).match(self.OBJECT, name=object_to_remove).first()
        if object_node:
            self.graph.delete(object_node)

    def remove_tag(self, tag_to_remove: str):
        tag = NodeMatcher(self.graph).match(self.TAG, name=tag_to_remove).first()
        if tag:
            self.graph.delete(tag)


    def close(self):
        pass

