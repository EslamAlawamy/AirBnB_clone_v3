#!/usr/bin/python3
""" Contains CRUD operations for amenity resources """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.get('/amenities')
def get_amenities():
    """ Reads amenities """
    amenities = [
        amenity.to_dict()
        for amenity in storage.all(Amenity).values()
    ]

    return jsonify(amenities)


@app_views.get('/amenities/<amenity_id>')
def get_amenity(amenity_id):
    """ Reads amenity """
    amenity = storage.get(Amenity, amenity_id)

    if amenity:
        return jsonify(amenity.to_dict())

    abort(404)


@app_views.delete('/amenities/<amenity_id>')
def delete_amenity(amenity_id):
    """ Deletes amenity """
    amenity = storage.get(Amenity, amenity_id)

    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({})

    abort(404)


@app_views.post('/amenities')
def post_amenity():
    """ Create amenity """
    data = request.get_json()

    if not data:
        abort(400, 'Not a JSON')

    if data.get('name', None):
        amenity = Amenity(**data)
        amenity.save()
        return jsonify(amenity.to_dict()), 201

    abort(400, 'Missing name')


@app_views.put('/amenities/<amenity_id>')
def put_amenity(amenity_id):
    """ Updates amenity """
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    data = request.get_json()

    if not data:
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'created_at', 'updated_at']

    for k, v in data.items():
        if k not in ignore_keys:
            setattr(amenity, k, v)

    amenity.save()
    return jsonify(amenity.to_dict())
