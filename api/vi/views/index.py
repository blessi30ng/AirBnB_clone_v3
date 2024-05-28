#!/usr/bin/python3

from api.v1.views import app_views

@app_views.route('/status', methods=['GET'],  strict_slashes=False)
def status():
	"""Status of API"""
	return jsonify({"status" : "OK")

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def no_of_objscts():
	"""retrieves no. of objs """
	return jsonify({
		"amenities": storage.count("Amenity"),
		"cities": storage.count("City"),
		"places": storage.count("Place"),
		"reviews": storage.count("Review"),
		"states": storage.count("State"),
		"users": storage.count("User"),
	})
