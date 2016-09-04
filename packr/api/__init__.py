from flask import Blueprint
from flask_restplus import Api
from packr.api.user import api as UserNS

blueprint = Blueprint('api', __name__)
api = Api(blueprint,
          title='Packr',
          version='0.0.1',
          description='For sending packages')
api.add_namespace(UserNS)
