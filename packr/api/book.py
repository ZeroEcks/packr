import json
import re

import datetime

import dateutil
from flask_restplus import Namespace, Resource, fields, reqparse
from flask_jwt import current_identity, jwt_required

from packr.models import Contact, Address, Order, Package, DangerClass, \
    ServiceType

api = Namespace('book',
                description='Operations related to creating a booking')

booking = api.model('Book', {
    'type': fields.String(readOnly=True,
                          descriptuon='The service type'),
    'dangerous': fields.String(readOnly=True,
                               description='The danger type, if applicable'),
    'pickup': fields.String(readOnly=True,
                            description='The pickup data'),
    'delivery': fields.String(readOnly=True,
                              description='The delivery data'),
    'fragile': fields.String(readonly=True,
                             description="If the package is fragile"),
    'paymentType': fields.String(readOnly=True,
                                 description='The payment type'),
    'customerComments': fields.String(readOnly=True,
                                      description='The customer comments'),
    'packages': fields.String(readOnly=True,
                              description='A JSON map of the packages')
})


@api.route('/')
class BookItem(Resource):
    @api.expect(booking)
    @api.response(204, 'Created booking.')
    @jwt_required()
    def post(self):
        req_parse = reqparse.RequestParser(bundle_errors=True)
        req_parse.add_argument('type', type=str,
                               help='No service type provided',
                               required=True,
                               location='json')
        req_parse.add_argument('dangerous', type=str,
                               required=False,
                               location='json')
        req_parse.add_argument('delivery', type=str, required=True,
                               help='No delivery data provided',
                               location='json')
        req_parse.add_argument('pickup', type=str, required=True,
                               help='No pickup data provided',
                               location='json')
        req_parse.add_argument('fragile', type=str, required=True,
                               help='No fragile status provided',
                               location='json')
        req_parse.add_argument('paymentType', type=str, required=True,
                               help='No payment type provided',
                               location='json')
        req_parse.add_argument('customerComments', type=str, required=False,
                               location='json')
        req_parse.add_argument('packages', type=str, required=True,
                               help='No packages list provided',
                               location='json')

        args = req_parse.parse_args()

        service_type_name = args.get('type')
        dangerous = args.get('dangerous')

        pickup = json.loads(args.get('pickup'))

        delivery = json.loads(args.get('delivery'))

        fragile = args.get('fragile')
        payment_type_name = args.get('paymentType')
        comments = args.get('customerComments')

        packages = json.loads(args.get('packages'))

        if pickup['businessName'] == '':
            return {'message': {
                'email': 'No pickup business name provided'}}, 400

        if pickup['contactName'] == '':
            return {'message': {
                'email': 'No pickup contact name provided'}}, 400

        if pickup['phone'] == '':
            return {'message': {
                'email': 'No pickup phone provided'}}, 400

        if pickup['email'] == '':
            return {'message': {'email': 'No pickup email provided'}}, 400
        elif not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
                          pickup['email']):
            return {'message': {'email': 'Invalid pickup email provided'}}, 400

        if pickup['street'] == '':
            return {'message': {
                'email': 'No pickup street provided'}}, 400

        if pickup['suburb'] == '':
            return {'message': {
                'email': 'No pickup suburb provided'}}, 400

        if pickup['state'] == '':
            return {'message': {
                'email': 'No pickup state provided'}}, 400

        if pickup['postCode'] == '':
            return {'message': {
                'email': 'No pickup post code provided'}}, 400

        if pickup['dateTime'] == '':
            return {'message': {
                'email': 'No pickup date time provided'}}, 400

        if delivery['businessName'] == '':
            return {'message': {
                'email': 'No delivery business name provided'}}, 400

        if delivery['contactName'] == '':
            return {'message': {
                'email': 'No delivery contact name provided'}}, 400

        if delivery['phone'] == '':
            return {'message': {
                'email': 'No delivery phone provided'}}, 400

        if delivery['email'] == '':
            return {'message': {'email': 'No delivery email provided'}}, 400
        elif not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
                          delivery['email']):
            return {'message': {
                'email': 'Invalid delivery email provided'}}, 400

        if delivery['street'] == '':
            return {'message': {
                'email': 'No delivery street provided'}}, 400

        if delivery['suburb'] == '':
            return {'message': {
                'email': 'No delivery suburb provided'}}, 400

        if delivery['state'] == '':
            return {'message': {
                'email': 'No delivery state provided'}}, 400

        if delivery['postCode'] == '':
            return {'message': {
                'email': 'No delivery post code provided'}}, 400

        if fragile == '':
            return {'message': {
                'email': 'No fragility provided'}}, 400

        if payment_type_name == '':
            return {'message': {
                'email': 'No payment type provided'}}, 400

        if comments == '':
            return {'message': {
                'email': 'No comments provided'}}, 400

        if not packages:
            return {'message': {'email': 'No packages provided'}}, 400

        pickup_contact = Contact(business_name=pickup['businessName'],
                                 contact_name=pickup['contactName'],
                                 phone=pickup['phone'],
                                 email=pickup['email'])
        delivery_contact = Contact(business_name=delivery['businessName'],
                                   contact_name=delivery['contactName'],
                                   phone=delivery['phone'],
                                   email=delivery['email'])
        pickup_address = Address(street=pickup['street'],
                                 suburb=pickup['suburb'],
                                 state=pickup['state'],
                                 post_code=pickup['postCode'])
        delivery_address = Address(street=delivery['street'],
                                   suburb=delivery['suburb'],
                                   state=delivery['state'],
                                   post_code=delivery['postCode'])

        pickup_contact.save()
        delivery_contact.save()
        pickup_address.save()
        delivery_address.save()

        package_list = list()

        weight = 0

        for package in packages:
            new_package = Package(weight=package['weight'],
                                  width=package['width'],
                                  height=package['height'],
                                  length=package['length'])
            package_list.append(new_package)

            weight += float(package['weight'])

        danger_class = DangerClass.query.filter_by(name=dangerous).first()
        service_type = ServiceType.query.filter_by(name=
                                                   service_type_name).first()

        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"

        eta = datetime.date.today()
        if service_type_name == 'overnight':
            eta += datetime.timedelta(days=1)
        elif service_type.name == 'express':
            eta += datetime.timedelta(days=3)
        else:
            eta += datetime.timedelta(days=5)

        new_order = Order(created_at=datetime.datetime.utcnow(),
                          cost=0,
                          delivery_address=delivery_address,
                          pickup_address=pickup_address,
                          delivery_contact=delivery_contact,
                          pickup_contact=pickup_contact,
                          package=package_list,
                          weight=weight,
                          fragile=(fragile == 'yes'),
                          danger=danger_class,
                          user_id=current_identity.id,
                          notes=comments,
                          service_type=service_type,
                          payment_type=payment_type_name,
                          eta=eta,
                          pickup_time=datetime.datetime.strptime(
                              pickup['dateTime'],
                              date_format))

        new_order.save()

        return {'message': {
            'description': 'Successfully booked pickup.`'}}, 201
