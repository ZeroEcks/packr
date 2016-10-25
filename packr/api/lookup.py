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
            statuses.append({'status': status.status,
                             'date': status.time.strftime('%Y-%m-%dT%H:%M:%S'),
                             'address': status.address})

        pickup = {
            'street': order.pickup_address.street,
            'suburb': order.pickup_address.suburb,
            'state': order.pickup_address.state,
            'postCode': order.pickup_address.post_code
        }

        delivery = {
            'street': order.delivery_address.street,
            'suburb': order.delivery_address.suburb,
            'state': order.delivery_address.state,
            'postCode': order.delivery_address.post_code
        }

        return {'eta': order.eta.strftime('%Y-%m-%dT%H:%M:%S'),
                'delivery': delivery,
                'pickup': pickup,
                'statuses': statuses}, 201
