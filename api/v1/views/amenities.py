#!/usr/bin/python3
""" handles all default restful API for amenities """

from models.amenity import Amenity
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def list_of_amenities():
        """ Return all amenities """
        l_amenities = []
        all_amenity = storage.all("Amenity").values()
        for amenity in all_amenity:
                l_amenities.append(amenity.to_dict())
        return jsonify(l_amenities)

@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
        """ retrieves a specific amenity """
        amenity = storage.get("Amenity", amenity_id)
        if not amenity:
                abort(404)

        return jsonify(amenity.to_dict())

app_views.route('/amenities/amenity_id>', methods=['GET'], strict_slashes=False)
def del_amenity(amenity_id):
        """ deletes a specific amenity """
        amenity = storage.get("Amenity", amenity_id)
        if not amenity:
                abort(404)

        storage.delete(amenity)
        storage.save()

        return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def new_amenity(amenity_id):
        """ Creates an amenity """
        if not request.get_json():
                abort(400, description="Not a JSON")

        if not request.get_json().get('name'):
                abort(400, description="Missing name")

        instance = Amenity()
        instance.name = request.get_json().get('name')
        instance.save()

        return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
        """ updates an amenity """
        amenity = storage.get("Amenity", amenity_id)
        if not amenity:
                abort(404)

        if not request.get_json():
                abort(400, description="Not a JSON")

        ignored = ["id", "created_at", "updated_at"]
        for key, value in request.get_json().items():
                if key not in ignored:
                        setattr(amenity, key, value)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
