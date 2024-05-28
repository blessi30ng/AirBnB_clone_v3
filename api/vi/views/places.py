#!/usr/bin/python3
""" handles all default restful API for places """

from models.place import Place
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def list_of_places(city_id):
        """ Return all places """
        l_places = []
        city = storage.get("City", city_id)
        if not city:
                abort(404)
        for place in storage.all("Place").values():
		if place.city_id == city_id:
                	l_places.append(place.to_dict())
        return jsonify(l_places)

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
        """ retrieves a specific place """
        place = storage.get("Place", place_id)
        if not place:
                abort(404)

        return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def del_place(place_id):
        """ deletes a specific place """
        place = storage.get("Place", place_id)
        if not place:
                abort(404)

        storage.delete(place)
        storage.save()

        return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def new_place(city):
        """ Creates a new place """
        if not storage.get("City", city_id):
                abort(404)

        if not request.get_json():
                abort(400, description="Not a JSON")

        if not request.get_json().get('name'):
                abort(400, description="Missing name")
	
	if not request.get_json().get('user_id'):
		abort(400, description="Missing user_id")

	if not storage.get("User", user_id):
		abort(404)
        instance = Place()
        instance.name = request.get_json().get('name')
        instance.city_id = city_id
	instance.user_id = user_id
        instance.save()

        return make_response(jsonify(instance.to_dict()), 201)




@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def place_city(place_id):
        """ updates a place """
        place = storage.get("Place", place_id)
        if not place:
                abort(404)

        if not request.get_json():
                abort(400, description="Not a JSON")

        ignored = ["id", "city_id", "user_id", "created_at", "updated_at"]
        for key, value in request.get_json().items():
                if key not in ignored:
                        setattr(place, key, value)
        storage.save()
        return make_response(jsonify(place.to_dict()), 200)
