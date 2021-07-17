import logging

from app.create_app import create_app
from app.settings import Settings


try:
    app_settings = Settings(_env_file='.env')
    storage_settings = app_settings.tag_storage_settings
    tag_store = storage_settings.get_storage()
except Exception as e:
    logging.getLogger('root').exception(e)
    raise e
app = create_app(tag_store, app_settings.app_name)
