#!/usr/bin/python3
""" Contains CRUD operations for reviews resources """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews(place_id):
    """ Reads reviews """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    reviews = [
        review.to_dict()
        for review in place.reviews
    ]

    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """ Reads review """
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """ Deletes review """
    review = storage.get(Review, review_id)

    if review:
        storage.delete(review)
        storage.save()
        return jsonify({})

    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def post_review(place_id):
    """ Creates review """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    data = request.get_json()

    if not data:
        abort(400, 'Not a JSON')

    if 'user_id' not in data:
        abort(400, 'Missing user_id')

    user = storage.get(User, data.get('user_id'))

    if not user:
        abort(404)

    if 'text' not in data:
        abort(400, 'Missing text')

    data['place_id'] = place_id
    review = Review(**data)
    review.save()

    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def put_review(review_id):
    """ Updates review """
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    data = request.get_json()

    if not data:
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    for k, v in data.items():
        if k not in ignore_keys:
            setattr(review, k, v)

    review.save()
    return jsonify(review.to_dict())
