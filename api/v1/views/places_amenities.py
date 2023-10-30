#!/usr/bin/python3
""" Contains CRUD operations for place_amenities resources """
from os import getenv
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_place_amenities(place_id):
    """ Reads place_amenty """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenities = [
        amenity.to_dict()
        for amenity in place.amenities
    ]

    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """ Deletes place_amenity """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity in place.amenities:
            place.amenities.remove(amenity)
            place.save()
            return jsonify({})
    else:
        if amenity_id in place.amenity_ids:
            place.amenities_ids.remove(amenity_id)
            place.save()
            return jsonify({})

    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def post_place_amenity(place_id, amenity_id):
    """ Creates place_amenity """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity not in place.amenities:
            place.amenities.append(amenity)
            place.save()
            return jsonify(amenity), 201
    else:
        if amenity_id not in place.amenity_ids:
            place.amenity_ids.append(amenity_id)
            place.save()
            return jsonify(amenity), 201

    return jsonify(amenity)
