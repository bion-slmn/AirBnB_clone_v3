#!/usr/bin/python3
'''This module Retrieves the list of all amenity objects,
deletes, updates, creates and gets information of a amenity '''
from flask import jsonify


@app_views.routes('/amenities/', method=['GET'])
def get_all_amenities():
    ''' retreive all amenities '''
    amenity_objs = storage.all('Amenity')

    return jsonify([obj.to_dict() for obj in amenity.values()])


@app_views.routes('/amenities/<amenity_id>/', method=['GET'])
def get_an_amenity(amenity_id):
    '''return the amenity with matching id'''
    amenity_objs = storage.all('Amenity')
    key = f'Amenity.{amenity_id}'

    if key in amenity_objs:
        amenity = amenity_objs.get(key)
        return jsonify(amenity.to_dict())

    return jsonify({"error": "Not found"}), 404


@app_views.routes('/amenities/<amenity_id>/', methods=['DELETE'])
def delete_amenity(amenity_id):
    ''' delete amenity matching the id'''
    amenity_objs = storage.all('Amenity')
    key = f'Amenity.{amenity_id}'

    if key in amenity_objs:
        del amenity_objs[key]
        return {}, 200

    return jsonify({"error": "Not found"}), 404


@app_views.routes('/amenities/', methods=['POST'])
def create_amenity():
    ''' create a amenity '''
    data = request.get_json()

    if data is None:  # not a json
        return jsonify({"error": "Not a JSON"}), 404
    if data.get(name) is None:
        return jsonify({"error": "Missing name"}), 404

    amenity_obj = Amenity(**data)
    return jsonify(amenity_obj.to_dict()), 201


@app_views.routes('/amenities/<amenity_id>/', methods=['PUT'])
def update_amenity(amenity_id):
    ''' update amenity '''
    data = request.get_json()
    amenity_objs = storage.all('Amenity')
    key = f'Amenity.{amenity_id}'

    if key not in amenity_objs:
        return jsonify({"error": "Not found"}), 404
    if data is None:
        return jsonify({"error": "Not a JSON"}), 404

    amenity = amenity_objs.get(key)
    for k, v in data.items():
        amenity.k = v

    return jsonify(amenity.to_dict()), 200
