#!/usr/bin/python3
""" Contains CRUD operations for users resources """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.get('/cities/<city_id>/places')
def get_places(city_id):
    """ Reads places """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    places = [
        place.to_dict()
        for place in storage.all(Place) if place.city_id == city_id
    ]

    return jsonify(places)


@app_views.get('/places/<place_id>')
def get_place(place_id):
    """ Reads place """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.delete('/places/<place_id>')
def delete_place(place_id):
    """ Deletes place """
    place = storage.get(Place, place_id)

    if place:
        storage.delete(place)
        storage.save()
        return jsonify({})

    abort(404)


@app_views.post('/cities/<city_id>/places')
def post_place(city_id):
    """ Creates place """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    data = request.get_json()

    if not data:
        abort(400, 'Not a JSON')

    if 'user_id' not in data:
        abort(400, 'Missing user_id')

    user = storage.get(User, data.get('user_id'))

    if not user:
        abort(404)

    if 'name' not in data:
        abort(400, 'Missing name')

    data['city_id'] = city_id

    place = Place(**data)
    place.save()

    return jsonify(place.to_dict()), 201


@app_views.put('/places/<place_id>')
def put_place(place_id):
    """ Updates place """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    data = request.get_json()

    if not data:
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for k, v in data:
        if k not in ignore_keys:
            setattr(place, k, v)

    place.save()
    return jsonify(place)
