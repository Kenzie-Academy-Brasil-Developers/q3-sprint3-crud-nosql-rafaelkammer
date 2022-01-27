from xml.dom import NotFoundErr
import pymongo
from bson.objectid import ObjectId
from datetime import datetime as dt

client = pymongo.MongoClient('mongodb://localhost:27017')

db = client['kenzie']

class Post:
    def __init__(self, *args, **kwargs) -> None:
        self.created_at = dt.now().strftime("%d/%m/%Y %H:%M:%S")
        self.updated_at = dt.now().strftime("%d/%m/%Y %H:%M:%S")
        self.title = kwargs['title']
        self.author = kwargs['author']
        self.tags = kwargs['tags']
        self.content = kwargs['content']

    def insert_post(self):
        db.posts.insert_one(self.__dict__)

    @staticmethod
    def update_post(post_id, data):

        keys = ["title", "author", "tags", "content"]

        if not all(key in data for key in keys):
            raise KeyError

        update_target = db.posts.find_one_and_update({"_id": ObjectId(post_id)}, {"$set": data})

        if update_target == None:
            raise NotFoundErr

        return update_target

    @staticmethod
    def exclude_post(post_id):
        excluded_post = db.posts.find_one_and_delete({"_id": ObjectId(post_id)})
        
        if excluded_post == None:
            raise NotFoundErr

        return excluded_post

    @staticmethod
    def serialize_post(data):
        if type(data) is list:
            for post in data:
                post.update({"_id": str(post["_id"])})
        elif type(data) is Post:        
            data._id = str(data._id)
        elif type(data) is dict:
            data.update({"_id": str(data["_id"])})

    @staticmethod
    def get_all():
        post_list = db.posts.find()
        return post_list

    @staticmethod
    def get_one(post_id):
        post = db.posts.find_one({"_id": ObjectId(post_id)})

        if post == None:
            raise NotFoundErr

        return post
    