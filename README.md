# tagapi
A tagging api

This project provides an API to tag objects. It allows you to tag/untag objects with multiple tags, ask for the objects with a certain tag, or the tags of an object.

Built with FastApi, it supports different storages for the tags and objects. At the moment there are only two implementations:
* One uses pickle and stores tags and objects in a file
* One uses py2neo and stores tags and objects as a bipartite graph

To run it:

```
pip install -r requirements.txt
cp .env.example.pickle_db .env
python -m uvicorn main:app
```
After that, navigate to 127.0.0.1:8000/docs to see the openapi documentation of the endpoints.
