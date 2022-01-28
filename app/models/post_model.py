from xml.dom import NotFoundErr
import pymongo
from bson.objectid import ObjectId
from datetime import datetime as dt

client = pymongo.MongoClient('mongodb://localhost:27017')

db = client['kenzie']

def last_id():
    post_list = list(db.posts.find())

    if not post_list:
        return 1
    else:
        return post_list[len(post_list) - 1]['id'] +1

class Post:

    current_id = last_id()

    def __init__(self, *args, **kwargs) -> None:
        self.created_at = dt.now().strftime("%d/%m/%Y %H:%M:%S")
        self.updated_at = dt.now().strftime("%d/%m/%Y %H:%M:%S")
        self.title = kwargs['title']
        self.author = kwargs['author']
        self.tags = kwargs['tags']
        self.content = kwargs['content']
        self.id = self.current_id

    def insert_post(self):
        db.posts.insert_one(self.__dict__)
        Post.current_id = last_id()

    @staticmethod
    def update_post(id, data):

        keys = ["title", "author", "tags", "content"]

        if not all(key in data for key in keys):
            raise KeyError

        update_target = db.posts.find_one_and_update({"id": int(id)}, {"$set": data}, return_document=True)

        if update_target == None:
            raise NotFoundErr

        return update_target

    @staticmethod
    def exclude_post(id):
        excluded_post = db.posts.find_one_and_delete({"id": int(id)})
        
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
    def get_one(id):
        post = db.posts.find_one({"id": int(id)})


        if post == None:
            raise NotFoundErr

        return post
    