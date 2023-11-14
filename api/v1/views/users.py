#!/usr/bin/python3
'''This module Retrieves the list of all user objects,
deletes, updates, creates and gets information of a user '''
from flask import jsonify


def error(message):
    '''create an error message and jsonify it '''
    return jsonify({"error" : message})


@app_views.routes('/user/', method=['GET'])
def get_all_user():
    ''' retreive all user '''
    user_objs = storage.all('User')

    return jsonify([obj.to_dict() for obj in user.values()])


@app_views.routes('/user/<user_id>/', method=['GET'])
def get_a_user(user_id):
    '''return the user with matching id'''
    user_objs = storage.all('User')
    key = f'User.{user_id}'

    if key in user_objs:
        user = user_objs.get(key)
        return jsonify(user.to_dict())

    return error('Not found'), 404


@app_views.routes('/user/<user_id>/', methods=['DELETE'])
def delete_user(user_id):
    ''' delete user matching the id'''
    user_objs = storage.all('User')
    key = f'User.{user_id}'

    if key in user_objs:
        del user_objs[key]
        return {}, 200

    return error('Not found'), 404


@app_views.routes('/user/', methods=['POST'])
def create_user():
    ''' create a user '''
    data = request.get_json()

    if data is None:  # not a json
        return error("Not a JSON"), 404
    if data.get(name) is None:
        return error("Missing name"), 404

    user_obj = User(**data)
    return jsonify(user_obj.to_dict()), 201


@app_views.routes('/user/<user_id>/', methods=['PUT'])
def update_user(user_id):
    ''' update user  whose id is passed'''
    data = request.get_json()
    user_objs = storage.all('User')
    key = f'User.{user_id}'

    if key not in user_objs:
        return error("Not found"), 404
    if data is None:
        return error("Not a JSON"), 404

    user = user_objs.get(key)
    for k, v in data.items():
        user.k = v

    return jsonify(user.to_dict()), 200
