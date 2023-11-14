#!/usr/bin/python3
'''This module Retrieves the list of all City objects,
deletes, updates, creates and gets information of a city '''
from flask import jsonify


@app_views.routes('/states/<state_id>/cities/', method=['GET'])
def get_all_cities(state_id):
    ''' retreive all city associted with the state obj'''
    state_objs = storage.all('State')
    key = f'State.{state_id}'

    if key in state_objs:
        state = state_objs.get(key)
        return jsonify([obj.to_dict() for obj in state.cities])

    return jsonify({"error": "Not found"}), 404


@app_views.routes('/cities/<city_id>/', method=['GET'])
def get_a_cities(city_id):
    '''return the city with matching id'''
    city_objs = storage.all('City')
    key = f'City.{city_id}'

    if key in city_objs:
        city = city_objs.get(key)
        return jsonify(city.to_dict())

    return jsonify({"error": "Not found"}), 404


@app_views.routes('/cities/<city_id>/', methods=['DELETE'])
def delete_a_cities(city_id):
    ''' delete a city matching the id'''
    city_objs = storage.all('City')
    key = f'City.{city_id}'

    if key in city_objs:
        del city_objs[key]
        return {}, 200

    return jsonify({"error": "Not found"}), 404


@app_views.routes('/states/<state_id>/cities/', methods=['POST'])
def create_a_cities(state_id):
    ''' create a city '''
    data = request.get_json()
    state_objs = storage.all('State')
    key = f'State.{state_id}'

    if key not in state_objs:
        return jsonify({"error": "Not found"}), 404
    if data is None:  # not a json
        return jsonify({"error": "Not a JSON"}), 404
    if data.get(name) is None:
        return jsonify({"error": "Missing name"}), 404

    city_obj = City(**data)
    state_objs[key].cities.append(city_obj)
    return jsonify(city_obj.to_dict()), 201


@app_views.routes('/cities/<city_id>/', methods=['PUT'])
def update_a_cities(city_id):
    ''' update a city '''
    data = request.get_json()
    city_objs = storage.all('City')
    key = f'City.{city_id}'

    if key not in city_objs:
        return jsonify({"error": "Not found"}), 404
    if data is None:
        return jsonify({"error": "Not a JSON"}), 404

    city = city_objs.get(key)
    for k, v in data.items():
        city.k = v

    return jsonify(city.to_dict()), 200
