# tagapi
A tagging api

This project provides an API to tag objects. It allows you to tag/untag objects with multiple tags, ask for the objects with a certain tag, or the tags of an object.

Built with FastApi, it will support different storages for the tags and objects. At the moment there is only one implementation based on piclke files.

To run it:

```
pip install -r requirements.txt
cp .env.example.pickle_db .env
python -m uvicorn main:app
```
After that, navigate to 127.0.0.1:8000/docs to see the openapi documentation of the endpoints.
