#!/usr/bin/python3
""" handles all default restful API for cities """

from models.city import City
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def list_of_cities(state_id):
        """ Return all cities """
        l_cities = []
        state = storage.get(State, state_id)
	if not state:
		abort(404)
	for city in state.cities:
                l_cities.append(city.to_dict())
        return jsonify(l_cities)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
        """ retrieves a specific city """
        city = storage.get("City", city_id)
        if not city:
                abort(404)

        return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
	""" deletes a specific city """
	city = storage.get("City", city_id)
        if not city:
                abort(404)

        storage.delete(city)
        storage.save()

        return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def new_city(state_id):
        """ Creates a new city """
	if not storage.get("State", state_id):
		abort(404)

        if not request.get_json():
                abort(400, description="Not a JSON")

        if not request.get_json().get('name'):
                abort(400, description="Missing name")

        instance = City()
        instance.name = request.get_json().get('name')
	instance.state_id = state_id
        instance.save()

	return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
	""" updates a city """
	city = storage.get("City", city_id)
        if not city:
                abort(404)

        if not request.get_json():
                abort(400, description="Not a JSON")
	
	ignored = ["id", "state_id", "created_at", "updated_at"]
        for key, value in request.get_json().items():
                if key not in ignored:
                        setattr(city, key, value)
        storage.save()
        return make_response(jsonify(city.to_dict()), 200)
