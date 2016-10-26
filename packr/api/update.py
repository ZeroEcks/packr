import datetime
import json

from flask.ext.jwt import jwt_required, current_identity
from flask_restplus import Namespace, Resource, fields, reqparse

from packr.models import Order, OrderStatus, StatusType

api = Namespace('update',
                description='Operations related to updating an order')

update_status = api.model('UpdateStatus', {
    'con_number': fields.Integer(readOnly=True,
                                 description='The consignment number'),
    'status': fields.String(readOnly=True,
                            description='The new status')
})

update_driver = api.model('UpdateDriver', {
    'con_number': fields.Integer(readOnly=True,
                                 description='The consignment number'),
    'adminComments': fields.String(readOnly=True,
                                   description='The admin comments')
})

update_admin = api.model('UpdateAdmin', {
    'con_number': fields.Integer(readOnly=True,
                                 description='The consignment number'),
    'driver': fields.String(readOnly=True,
                            description='The driver'),
    'eta': fields.String(readOnly=True,
                         description='The eta'),
    'cost': fields.String(readOnly=True,
                          description='The cost')
})


@api.route('/status')
class UpdateStatus(Resource):
    @api.expect(update_status)
    @api.response(204, 'Successfully updated status.')
    @jwt_required()
    def post(self):
        req_parse = reqparse.RequestParser(bundle_errors=True)
        req_parse.add_argument('con_number', type=int, required=True,
                               location='json')
        req_parse.add_argument('status', type=str, required=True,
                               location='json')

        args = req_parse.parse_args()

        con_number = args.get('con_number', -1)
        status = json.loads(args.get('status'))

        if con_number == -1:
            return {'message': {'con_number':
                                'No consignment number provided'}}, 400

        # Find the consignment note information.
        order = Order.query.filter_by(id=con_number).first()
        if not order:
            return {'description': 'Unknown consignment number.'}, 404

        if current_identity.role.role_name != 'admin':
            if current_identity.role.role_name == 'driver':
                if order.driver_id != current_identity.id:
                    return {'description': 'Access denied.'}, 401
            else:
                return {'description': 'Access denied.'}, 401

        status_type = StatusType.query.filter_by(name=status['status']).first()

        order_status = OrderStatus(status=status_type,
                                   address=status['address'],
                                   time=datetime.datetime.utcnow(),
                                   order_id=order.id)

        order_status.save()

        order.status.append(order_status)
        order.save()

        return {'message': {'description': 'Updated status'}}, 201


@api.route("/admin")
class UpdateAdmin(Resource):
    @api.expect(update_admin)
    @api.response(204, 'Successfully updated admin details.')
    @jwt_required()
    def post(self):
        req_parse = reqparse.RequestParser(bundle_errors=True)
        req_parse.add_argument('con_number', type=int, required=True,
                               location='json')
        req_parse.add_argument('driver', type=str, required=True,
                               location='json')
        req_parse.add_argument('eta', type=str, required=True,
                               location='json')
        req_parse.add_argument('cost', type=int, required=True,
                               location='json')

        args = req_parse.parse_args()

        con_number = args.get('con_number', -1)
        driver = args.get('driver', None)
        eta = args.get('eta')
        cost = args.get('cost', 0)

        if con_number == -1:
            return {'message': {'con_number':
                                'No consignment number provided'}}, 400

        if current_identity.role.role_name != 'admin':
            return {'description': 'Access denied.'}, 401

        # Find the consignment note information.
        order = Order.query.filter_by(id=con_number).first()
        if not order:
            return {'description': 'Unknown consignment number.'}, 404

        order.driver_id = driver
        order.cost = cost
        order.eta = datetime.datetime.strptime(eta, "%Y-%m-%dT%H:%M:%S.%fZ") \
            .date()

        order.save()

        return {'message': {'description': 'Updated consignment'}}, 201


@api.route("/driver")
class UpdateDriver(Resource):
    @api.expect(update_driver)
    @api.response(204, 'Successfully updated driver details.')
    @jwt_required()
    def post(self):
        req_parse = reqparse.RequestParser(bundle_errors=True)
        req_parse.add_argument('con_number', type=int, required=True,
                               location='json')
        req_parse.add_argument('adminComments', type=str, required=True,
                               location='json')

        args = req_parse.parse_args()

        con_number = args.get('con_number', -1)
        admin_comments = args.get('adminComments')

        if con_number == -1:
            return {'message': {'con_number':
                                'No consignment number provided'}}, 400

        # Find the consignment note information.
        order = Order.query.filter_by(id=con_number).first()
        if not order:
            return {'description': 'Unknown consignment number.'}, 404

        if current_identity.role.role_name != 'admin':
            if current_identity.role.role_name == 'driver':
                if order.driver_id != current_identity.id:
                    return {'description': 'Access denied.'}, 401
            else:
                return {'description': 'Access denied.'}, 401

        order.driver_notes = admin_comments

        order.save()

        return {'message': {'description': 'Updated consignment'}}, 201
