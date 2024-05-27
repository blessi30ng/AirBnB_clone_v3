#!/usr/bin/python3
""" handles all default restful API for states """

from models.state import State
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def list_states():
	""" Return all states """
	l_states = []
	for state in storage.all("State").values():
		l_states.append(state.to_dict())
	return jsonify(l_states)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
	""" retrieves a specific state """
	state = storage.get("State", state_id)
	if not state:
		abort(404)

	return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def del_state(state_id):
	""" Deletes a state by id """
	state = storage.get("State", state_id)
	if not state:
		abort(404)

	storage.delete(state)
	storage.save()

	return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def new_state():
	""" Creates a new state """
	if not request.get_json():
		abort(400, description="Not a JSON")

	if not request.get_json().get('name'):
		abort(400, description="Missing name")
	
	instance = State()
	instance.name = request.get_json()['name']
	instance.save()

	return make_response(jsonify(instance.to_dict()), 201)

def update_state(state_id):
	""" updates a state """
	state = storage.get("State", state_id)
	if not state:
		abort(404)

	if not request.get_json():
		abort(400, description="Not a JSON")

	for key, value in request.get_json().items():
		if key == "id" or key == "created_at" or key == "updated_at":
			continue
		else:
			setattr(state, key, value)

	storage.save()
	return make_response(jsonify(state.to_dict()), 200)


