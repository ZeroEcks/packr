from flask import Blueprint
from flask_restplus import Api
from .user import api as user_api
from .quote import api as quote_api

blueprint = Blueprint('api', __name__)
api = Api(blueprint,
          title='Packr',
          version='0.0.1',
          description='For sending packages')
api.add_namespace(user_api)
api.add_namespace(quote_api)
