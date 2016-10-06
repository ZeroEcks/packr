import re

from flask import jsonify
from flask_restplus import Namespace, Resource, fields, reqparse
from sqlalchemy.exc import IntegrityError

from packr.models import Delivery

api = Namespace('delivery',
                description='Operations related to creating a delivery')

delivery = api.model('Delivery', {
    'id': fields.Integer(readOnly=True,
                         description='The unique identifier of a delivery'),
    'driver_notes': fields.String(required=False,
                               description='Delivery Notes'),
    'signature': fields.String(required=True,
                              description='Signature')
})


@api.route('/')
class DeliveryItem(Resource):

    @api.response(200, 'Returns the delivery')
    def get(self):
        delivery = Delivery.query.all()
        return jsonify([{
            'driver_notes': delivery.driver_notes,
            'signature': delivery.signature
        }])

    @api.expect(delivery)
    @api.response(204, 'Delivery successfully created.')
    def post(self):
        req_parse = reqparse.RequestParser(bundle_errors=True)
        req_parse.add_argument('driver_notes', type=str, location='json')
        req_parse.add_argument('signature', type=bool, required=True,
                               help='No signature provided',
                               location='json')
        args = req_parse.parse_args()

        driver_notes = args.get('driver_notes')
        signature = args.get('signature')

        new_delivery = Delivery(driver_notes=driver_notes,
                                signature=signature)

        try:
            new_delivery.save()
        except IntegrityError as e:
            print(e)
            return {
                       'description': 'User with given email already exists.'
                   }, 409
        except Exception as e:
            print(e)
            return {'description': 'Server encountered an error.'}, 500

        return {'delivery': new_delivery}, 201
