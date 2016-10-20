import json
import re

from flask_restplus import Namespace, Resource, fields, reqparse

api = Namespace('track',
                description='Operations related to tracking a package')

track = api.model('Track', {
    'con_number': fields.Integer(readOnly=True,
                                 description='The consignment number'),
})


@api.route('/')
class TrackItem(Resource):
    @api.expect(track)
    @api.response(204, 'Tracking package.')
    def post(self):
        req_parse = reqparse.RequestParser(bundle_errors=True)
        req_parse.add_argument('con_number', type=int, required=True,
                               location='json')

        args = req_parse.parse_args()

        con_number = args.get('con_number', default=-1)

        if con_number == -1:
            return {'message': {'con_number': 'No consignment number provided'}}, 400

        # Find the consignment note information.

        return {'eta': ""}, 201
