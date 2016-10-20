import json
import re

from flask_restplus import Namespace, Resource, fields, reqparse

api = Namespace('quote',
                description='Operations related to generating a quote')

quote = api.model('Quote', {
    'businessName': fields.String(readOnly=True,
                                  description='The name of the business'),
    'contactName': fields.String(readOnly=True,
                                 description='The contact name'),
    'phone': fields.String(readOnly=True,
                           description='The phone number'),
    'email': fields.String(readOnly=True,
                           description='The email address'),
    'type': fields.String(readOnly=True,
                          descriptuon='The service type'),
    'dangerous': fields.String(readOnly=True,
                               description='The danger type, if applicable'),
    'street': fields.String(readOnly=True,
                            description='The street name and number'),
    'suburb': fields.String(readOnly=True,
                            description='The suburb name'),
    'state': fields.String(readOnly=True,
                           description='The state'),
    'postCode': fields.Integer(readOnly=True,
                               description='The postal code'),
    'packages': fields.String(readOnly=True,
                              description='A JSON map of the packages')
})


@api.route('/')
class QuoteItem(Resource):
    @api.expect(quote)
    @api.response(204, 'Created quote.')
    def post(self):
        req_parse = reqparse.RequestParser(bundle_errors=True)
        req_parse.add_argument('businessName', type=str, required=False,
                               location='json')
        req_parse.add_argument('contactName', type=str, required=True,
                               help='No contact name provided',
                               location='json')
        req_parse.add_argument('phone', type=str, required=True,
                               help='No phone number provided',
                               location='json')
        req_parse.add_argument('email', type=str, required=True,
                               help='No email provided',
                               location='json')
        req_parse.add_argument('type', type=str, required=True,
                               help='No service type provided',
                               location='json')
        req_parse.add_argument('phone', type=str, required=False,
                               location='json')
        req_parse.add_argument('street', type=str, required=True,
                               help='No street provided',
                               location='json')
        req_parse.add_argument('suburb', type=str, required=True,
                               help='No suburb provided',
                               location='json')
        req_parse.add_argument('state', type=str, required=True,
                               help='No state provided',
                               location='json')
        req_parse.add_argument('postCode', type=int, required=True,
                               help='No postal code provided',
                               location='json')
        req_parse.add_argument('packages', type=str, required=True,
                               help='No packages list provided',
                               location='json')

        args = req_parse.parse_args()

        contactName = args.get('contactName')
        phone = args.get('phone')
        email = args.get('email')
        service_type = args.get('type')
        phone = args.get('phone')
        street = args.get('street')
        suburb = args.get('suburb')
        state = args.get('state')
        post_code = args.get('postCode')
        packages = json.loads(args.get('packages'))

        if contactName == '':
            return {'message': {'email': 'No contact name provided'}}, 400

        if phone == '':
            return {'message': {'email': 'No phone number provided'}}, 400

        if email == '':
            return {'message': {'email': 'No email provided'}}, 400
        elif not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
                          email):
            return {'message': {'email': 'Invalid email provided'}}, 400

        if service_type == '':
            return {'message': {'email': 'No service type provided'}}, 400

        if street == '':
            return {'message': {'email': 'No street provided'}}, 400

        if suburb == '':
            return {'message': {'email': 'No suburb provided'}}, 400

        if state == '':
            return {'message': {'email': 'No state provided'}}, 400

        if post_code == '':
            return {'message': {'email': 'No post code provided'}}, 400

        if not packages:
            return {'message': {'email': 'No packages provided'}}, 400

        print(packages)

        # Calculate the monies
        quote_amount = 0
        for package in packages:
            quote_amount += int(package['weight']) + int(package['width']) \
                            + int(package['height']) + int(package['length'])

        if service_type == 'express':
            quote_amount *= 2
        elif service_type == 'overnight':
            quote_amount *= 3
        elif service_type == 'dangerous':
            quote_amount *= 4

        return {'quote': quote_amount}, 201
