#!/usr/bin/python3

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='api_v1')

from api.v1.vieews.index import *