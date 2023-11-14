#!/usr/bin/python3
'''This module Retrieves the list of all place objects,
deletes, updates, creates and gets information of a place '''
from flask import jsonify


def error(message):
    '''create an error message and jsonify it '''
    return jsonify({"error" : message})


@app_views.routes('/cities/<city_id>/places/', method=['GET'])
def get_all_place(city_id):
    ''' retreive all place associated with the city id '''
    city_objs = storage.all('City')
    key = f'City.{city_id}'
    
    if key in city_objs:
        city = city_objs.get(key)
        return jsonify([obj.to_dict() for obj in city.places])
    
    return error('Not found'), 404


@app_views.routes('/place/<place_id>/', method=['GET'])
def get_a_place(place_id):
    '''return the place with matching id'''
    place_objs = storage.all('Place')
    key = f'Place.{place_id}'

    if key in place_objs:
        place = place_objs.get(key)
        return jsonify(place.to_dict())

    return error('Not found'), 404


@app_views.routes('/place/<place_id>/', methods=['DELETE'])
def delete_place(place_id):
    ''' delete place matching the id'''
    place_objs = storage.all('Place')
    key = f'Place.{place_id}'

    if key in place_objs:
        del place_objs[key]
        return {}, 200

    return error('Not found'), 404


@app_views.routes('/cities/<city_id>/places/', methods=['POST'])
def create_place(city_id):
    ''' create a place '''
    data = request.get_json()
    city_objs = storage.all('City')
    key = f'City.{city_id}'

    if key not in city_objs:
        return error('Not found'), 404
    if data is None:  # not a json
        return error("Not a JSON"), 404
    if data.get('user_id') is None:
        return error("Missing user_id"), 404

    user_objs = storage.all('User')
    user_id = user_objs.get('user_id')
    if f'User.{user_id}' not in user_objs:
        return error('Not found'), 404
    if data.get('name') is None:
        return error("Missing name"), 404

    place_obj = Place(**data)
    return jsonify(place_obj.to_dict()), 201


@app_views.routes('/place/<place_id>/', methods=['PUT'])
def update_place(place_id):
    ''' update place  whose id is passed'''
    data = request.get_json()
    place_objs = storage.all('Place')
    key = f'Place.{place_id}'

    if key not in place_objs:
        return error("Not found"), 404
    if data is None:
        return error("Not a JSON"), 404

    place = place_objs.get(key)
    for k, v in data.items():
        setattr(place, k, v)

    return jsonify(place.to_dict()), 200
