from flask_restplus import Namespace, Resource, fields, reqparse

from packr.models import Order

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

        delivery_address = "{0} {1} {2} {3}".format(
            order.delivery_address.street,
            order.delivery_address.suburb,
            order.delivery_address.state,
            order.delivery_address.post_code)

        pickup_address = "{0} {1} {2} {3}".format(
            order.pickup_address.street,
            order.pickup_address.suburb,
            order.pickup_address.state,
            order.pickup_address.post_code)

        return {'eta': order.eta.strftime('%Y-%m-%dT%H:%M:%S'),
                'delivery_address': delivery_address,
                'pickup_address': pickup_address,
                'statuses': statuses}, 201
