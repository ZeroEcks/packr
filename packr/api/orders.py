import datetime

from flask.ext.jwt import jwt_required, current_identity
from flask_restplus import Namespace, Resource, fields, reqparse

from packr.models import Order

api = Namespace('orders',
                description='Operations related to orders')

orders = api.model('Orders', {
})


@api.route('/')
class OrdersItem(Resource):
    @api.expect(orders)
    @api.response(204, 'Grabbed orders.')
    @jwt_required()
    def post(self):
        orders_list = list()

        orders_source = None
        if current_identity.role.role_name == 'user':
            orders_source = Order.query.filter_by(user_id=current_identity.id)
        elif current_identity.role.role_name == 'driver':
            orders_source = Order.query.filter_by(
                driver_id=current_identity.id)
        elif current_identity.role.role_name == 'admin':
            orders_source = Order.query

        for order in orders_source:
            last_update = datetime.datetime.fromtimestamp(0)
            for status in order.status:
                if status.time > last_update:
                    last_update = status.time
            orders_list.append({
                'createdAt': order.created_at.strftime('%Y-%m-%dT%H:%M:%S'),
                'cost': order.cost,
                'lastUpdate': last_update.strftime('%Y-%m-%dT%H:%M:%S'),
                'id': order.id
            })

        return {'orders': orders_list}, 201
