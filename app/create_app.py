from typing import List, cast, Dict

from fastapi import FastAPI

from tag_storage.base_storage.async_tag_storage import AsyncTagStorage
from tag_storage.base_storage.sync_tag_storage import SyncTagStorage
from tag_storage.base_storage.tag_storage import TagStorage


def create_app(tag_storage: TagStorage, app_name:str='Tagapi'):
    app = FastAPI(name=app_name, title=app_name)

    if isinstance(tag_storage, AsyncTagStorage):
        create_async_app(app, cast(AsyncTagStorage, tag_storage))
    elif isinstance(tag_storage, TagStorage):
        create_sync_app(app, tag_storage)
    else:
        raise ValueError("Unknown type of TagStorage %s", type(tag_storage))
    return app


def create_async_app(app: FastAPI, tag_store: AsyncTagStorage):
    @app.get("/tags", response_model=List[str], tags=["Tags"])
    async def get_tags(limit: int = 100, offset: int = 0) -> List[str]:
        ret = await tag_store.get_tags(limit, offset)
        return ret

    @app.get("/tags/{tag_name}/objects", response_model=List[str], tags=["Tags"])
    async def get_tagged_obects(tag_name: str, limit: int = 100, offset: int = 0) -> List[str]:
        ret = await tag_store.get_tagged_objects(tag_name, limit, offset)
        return ret

    @app.delete("/tags/{tag_name}", response_model=Dict, tags=["Tags"])
    async def delete_tag(tag_name: str) -> List[str]:
        await tag_store.remove_tag(tag_name)
        return {}

    @app.get("/objects", response_model=List[str], tags=["Tagged Objects"])
    async def get_objects(limit: int = 100, offset: int = 0) -> List[str]:
        ret = await  tag_store.get_objects(limit, offset)
        return ret

    @app.get("/objects/{object_name}/tags", response_model=List[str], tags=["Tagged Objects"])
    async def get_object_tags(object_name: str, limit: int = 100, offset: int = 0) -> List[str]:
        ret = await tag_store.get_object_tags(object_name, limit, offset)
        return ret

    @app.delete("/objects/{object_name}", response_model=Dict, tags=["Tagged Objects"])
    async def delete_object(object_name: str):
        await tag_store.get_object_tags(object_name)
        return {}

    @app.post("/objects/{object_name}/tags", response_model=Dict, tags=["Tagged Objects"])
    async def apply_tags(object_name: str, tags_to_add: List[str]):
        await tag_store.tag(object_name, tags_to_add)
        return {}

    @app.delete("/objects/{object_name}/tags", response_model=Dict, tags=["Tagged Objects"])
    async def remove_tags(object_name: str, tags_to_remove: List[str]):
        await tag_store.untag(object_name, tags_to_remove)
        return {}

    @app.on_event("shutdown")
    async def shutdown_event():
        await tag_store.close()


def create_sync_app(app: FastAPI, tag_store: SyncTagStorage):
    @app.get("/tags", response_model=List[str], tags=["Tags"])
    def get_tags(limit: int = 100, offset: int = 0) -> List[str]:
        ret = tag_store.get_tags(limit, offset)
        return ret

    @app.get("/tags/{tag_name}/objects", response_model=List[str], tags=["Tags"])
    def get_tagged_obects(tag_name: str, limit: int = 100, offset: int = 0) -> List[str]:
        ret = tag_store.get_tagged_objects(tag_name, limit, offset)
        return ret

    @app.delete("/tags/{tag_name}", response_model=Dict, tags=["Tags"])
    def delete_tag(tag_name: str) -> List[str]:
        tag_store.remove_tag(tag_name)
        return {}

    @app.get("/objects", response_model=List[str])
    def get_objects(limit: int = 100, offset: int = 0) -> List[str]:
        ret = tag_store.get_objects(limit, offset)
        return ret

    @app.get("/objects/{object_name}/tags", response_model=List[str])
    def get_object_tags(object_name: str, limit: int = 100, offset: int = 0) -> List[str]:
        ret = tag_store.get_object_tags(object_name, limit, offset)
        return ret

    @app.delete("/objects/{object_name}", response_model=Dict)
    def delete_object(object_name: str):
        tag_store.get_object_tags(object_name)
        return {}

    @app.post("/objects/{object_name}/tags", response_model=Dict)
    def apply_tags(object_name: str, tags_to_add: List[str]):
        tag_store.tag(object_name, tags_to_add)
        return {}

    @app.delete("/objects/{object_name}/tags", response_model=Dict)
    def remove_tags(object_name: str, tags_to_remove: List[str]):
        tag_store.untag(object_name, tags_to_remove)
        return {}

    @app.on_event("shutdown")
    def shutdown_event():
        tag_store.close()
