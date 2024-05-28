#!/usr/bin/python3
""" flask app"""

from models import storage 
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS
from flask import Flask, make_response, jsonify
from flasgger import Swagger
from flasgger.utils import swag_from


app = Flask(__name__)
app.config['JSONIFY_PRETTY_PRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})



app.teardown_appcontext
def close_db(self):
	"""close stroge"""
	storage.close()

app.errorhandler
def page_not_found(error):
	""" json error response """
	return make_response(jsonify({'error': 'Not found'}), 404)

app.config['SWAGGER'] = {
	'title': 'AirBnB clon Restful API',
	'uiversion': 3
}

Swagger(app)


if __name__ == '__main__':
	""" main """
	host = environ.get('HBNB_API_HOST')
	port = environ.get('HBNB_API_HOST')
	if not host:
		host = '0.0.0.0'
	if not port:
		port = '5000'
	app.run(host=host, port=port, treaded=True)
