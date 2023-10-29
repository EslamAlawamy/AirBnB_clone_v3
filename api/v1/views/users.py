#!/usr/bin/python3
""" Contains CRUD operations for users resources """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.get('/users')
def get_users():
    """ Reads users """
    users = [
        user.to_dict()
        for user in storage.all(User).values()
    ]

    return jsonify(users)


@app_views.get('/users/<user_id>')
def get_user(user_id):
    """ Reads user """
    user = storage.get(User, user_id)

    if user:
        return jsonify(user.to_dict())

    abort(404)


@app_views.delete('/users/<user_id>')
def delete_user(user_id):
    """ Deletes user """
    user = storage.get(User, user_id)

    if user:
        storage.delete(user)
        storage.save()
        return jsonify({})

    abort(404)


@app_views.post('/users')
def post_user():
    """ Create user """
    data = request.get_json()

    if not data:
        abort(400, 'Not a JSON')

    if 'email' not in data:
        abort(400, 'Missing email')

    if 'password' not in data:
        abort(400, 'Missing password')

    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.put('/users/<user_id>')
def put_user(user_id):
    """ Updates user """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    data = request.get_json()

    if not data:
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'email', 'created_at', 'updated_at']

    for k, v in data.items():
        if k not in ignore_keys:
            setattr(user, k, v)

    user.save()
    return jsonify(user.to_dict())
