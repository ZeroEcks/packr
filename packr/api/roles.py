import datetime

from flask.ext.jwt import jwt_required, current_identity
from flask_restplus import Namespace, Resource, fields, reqparse

from packr.models import Order, User, Role

api = Namespace('roles',
                description='Operations related to roles')

roles_get = api.model('RolesGet', {
})

roles_update = api.model('RolesUpdate', {
    'id': fields.Integer(readOnly=True,
                         descriptuon='The user ID'),
    'role': fields.String(readOnly=True,
                          description='The role name'),
})


@api.route('/get')
class RolesGetItem(Resource):
    @api.expect(roles_get)
    @api.response(204, 'Grabbed roles.')
    @jwt_required()
    def post(self):
        users_list = list()
        roles_list = list()

        if current_identity.role.role_name != 'admin':
            return {'description': 'Access denied.'}, 401

        for user in User.query:
            users_list.append({
                'id': user.id,
                'fullName': user.full_name,
                'email': user.email,
                'role': user.role.role_name
            })

        for role in Role.query:
            roles_list.append({
                'roleName': role.role_name
            })

        return {'users': users_list, 'roles': roles_list}, 201


@api.route('/update')
class RolesUpdateItem(Resource):
    @api.expect(roles_update)
    @api.response(204, 'Grabbed roles.')
    @jwt_required()
    def post(self):
        req_parse = reqparse.RequestParser(bundle_errors=True)
        req_parse.add_argument('id', type=int, required=True,
                               location='json')
        req_parse.add_argument('role', type=str, required=True,
                               location='json')

        args = req_parse.parse_args()

        user_id = args.get('id', -1)
        role = args.get('role')

        if current_identity.role.role_name != 'admin':
            return {'description': 'Access denied.'}, 401

        user = User.query.filter_by(id=user_id).first()
        if not user:
            return {'description': 'Unknown user.'}, 404

        role_object = Role.query.filter_by(role_name=role).first()
        if not role_object:
            return {'description': 'Unknown role.'}, 404

        user.role = role_object
        user.save()

        return {'message': {'description': 'Updated role'}}, 201
