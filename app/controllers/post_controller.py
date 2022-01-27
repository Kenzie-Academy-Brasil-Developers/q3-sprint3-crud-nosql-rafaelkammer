from xml.dom import NotFoundErr
from app.models.post_model import Post
from flask import jsonify, request
from http import HTTPStatus
from datetime import datetime as dt

def retrieve_all():
    posts_list = Post.get_all()

    posts_list = list(posts_list)

    Post.serialize_post(posts_list)

    return jsonify(posts_list), HTTPStatus.OK

def retrieve_one(post_id):

    try:
        post = Post.get_one(post_id)

        Post.serialize_post(post)

        return jsonify(post), HTTPStatus.OK

    except NotFoundErr:
        return {"msg": "Post not found."}, HTTPStatus.NOT_FOUND

def create_post():
    try:
        data = request.get_json()
        post = Post(**data)

        post.insert_post()
        Post.serialize_post(post)

        return jsonify(post.__dict__), HTTPStatus.CREATED
    
    except KeyError:
        return {"msg": "Incorrect data key entry"}, HTTPStatus.BAD_REQUEST

def delete_post(post_id):

    try:
        excluded_post = Post.exclude_post(post_id)
        Post.serialize_post(excluded_post)

        return jsonify(excluded_post), HTTPStatus.OK
    
    except NotFoundErr:
        return {"msg": "Post not found."}, HTTPStatus.NOT_FOUND

def update_post(post_id):

    try:
        data = request.get_json()
        data["updated_at"] = dt.now().strftime("%d/%m/%Y %H:%M:%S")

        update_target = Post.update_post(post_id, data)
        
        Post.serialize_post(update_target)

        return jsonify(update_target), HTTPStatus.OK
    
    except KeyError:
        return {"msg": "Incorrect data key entry"}, HTTPStatus.BAD_REQUEST
    except NotFoundErr:
        return {"msg": "Post not found"}, HTTPStatus.NOT_FOUND