from flask_jwt import jwt_required
from flask_restful import Resource


class TestApi(Resource):
    # All API HTTP Methods are JWT Protected

    decorators = [jwt_required()]

    def get(self):
        return {}, 200

    def put(self):
        return {}, 200

    def post(self):
        return {}, 201

    def delete(self):
        return {}, 200
