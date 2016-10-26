import datetime

from flask_restplus import Namespace, Resource, fields, reqparse

from packr.models import Order

api = Namespace('lookup',
                description='Operations related to looking up an order')

lookup = api.model('Lookup', {
    'con_number': fields.Integer(readOnly=True,
                                 description='The consignment number'),
})


@api.route('/')
class LookupItem(Resource):
    @api.expect(lookup)
    @api.response(204, 'Successfully looked up order.')
    def post(self):
        req_parse = reqparse.RequestParser(bundle_errors=True)
        req_parse.add_argument('con_number', type=int, required=True,
                               location='json')

        args = req_parse.parse_args()

        con_number = args.get('con_number', -1)

        if con_number == -1:
            return {'message': {'con_number':
                                'No consignment number provided'}}, 400

        # Find the consignment note information.
        order = Order.query.filter_by(id=con_number).first()
        if not order:
            return {'description': 'Unknown consignment number.'}, 404

        statuses = list()

        for status in order.status:
            statuses.append({
                'status': status.status.status,
                'date': status.time.strftime('%Y-%m-%dT%H:%M:%S'),
                'address': status.address
            })

        packages = list()

        for package in order.package:
            packages.append({
                'weight': package.weight,
                'length': package.length,
                'width': package.width,
                'height': package.height
            })

        pickup_date = datetime.date(year=order.pickup_time.year,
                                    month=order.pickup_time.month,
                                    day=order.pickup_time.day)

        pickup_time = datetime.time(hour=order.pickup_time.hour,
                                    minute=order.pickup_time.minute,
                                    second=order.pickup_time.second)

        pickup = {
            'businessName': order.pickup_contact.business_name,
            'contactName': order.pickup_contact.contact_name,
            'phone': order.pickup_contact.phone,
            'email': order.pickup_contact.email,
            'street': order.pickup_address.street,
            'suburb': order.pickup_address.suburb,
            'state': order.pickup_address.state,
            'postCode': order.pickup_address.post_code,
            'date': pickup_date.strftime('%Y-%m-%d'),
            'time': pickup_time.strftime('%H:%M:%S')
        }

        delivery = {
            'businessName': order.delivery_contact.business_name,
            'contactName': order.delivery_contact.contact_name,
            'phone': order.delivery_contact.phone,
            'email': order.delivery_contact.email,
            'street': order.delivery_address.street,
            'suburb': order.delivery_address.suburb,
            'state': order.delivery_address.state,
            'postCode': order.delivery_address.post_code
        }

        driver = ''
        if order.driver:
            driver = order.driver.full_name

        return {'eta': order.eta.strftime('%Y-%m-%d'),
                'type': order.service_type.name,
                'driver': driver,
                'cost': order.cost,
                'paymentType': order.payment_type,
                'fragile': ('yes' if order.fragile else 'no'),
                'delivery': delivery,
                'pickup': pickup,
                'customerComments': order.notes,
                'adminComments': order.driver_notes,
                'statuses': statuses,
                'packages': packages}, 201
