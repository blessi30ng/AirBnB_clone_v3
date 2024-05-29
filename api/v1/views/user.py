#!/usr/bin/python3
""" handles all default restful API for users """

from models.user import User
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_of_users(state_id):
        """ Return all users """
        l_users = []

        for user in storage.all("User").values():
                l_users.append(user.to_dict())
        return jsonify(l_users)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
        """ retrieves a specific user """
        user = storage.get("User", user_id)
        if not user:
                abort(404)

        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def del_user(user_id):
        """ deletes a specific user """
        user = storage.get("User", user_id)
        if not user:
                abort(404)

        storage.delete(user)
        storage.save()

        return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def new_user():
        """ Creates a new user """
        if not request.get_json():
                abort(404, description="Not a JSON")

        if not request.get_json().get('email'):
                abort(400, description="Missing email")

        if not request.get_json().get('password'):
                abort(400, description="Missing password")

        instance = User()
        instance.email = request.get_json().get['email']
	instance.password = request.get_json().get['password']
        instance.save()

        return make_response(jsonify(instance.to_dict()), 201)



@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
        """ updates a user """
        user = storage.get("User", user_id)
        if not user:
                abort(404)

        if not request.get_json():
                abort(400, description="Not a JSON")

        ignored = ["id", "email", "created_at", "updated_at"]
        for key, value in request.get_json().items():
                if key not in ignored:
                        setattr(user, key, value)
        storage.save()
        return make_response(jsonify(user.to_dict()), 200)
