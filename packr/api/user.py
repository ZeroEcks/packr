import re

from flask_restplus import Resource, fields, Namespace
from packr.models import User
from sqlalchemy.exc import IntegrityError
from flask_restplus import reqparse

api = Namespace('user',
                description='Operations related to the current user')


user = api.model('User', {
    'id': fields.Integer(readOnly=True,
                         description='The unique identifier of a user'),
    'firstname': fields.String(required=True,
                               description='First name'),
    'lastname': fields.String(required=True,
                              description='Last name'),
    'email': fields.String(required=True,
                           description='Login email'),
    'password': fields.Integer(required=False,
                               description='The login passord'),
})


@api.route('/')
class UserItem(Resource):

    @api.marshal_with(user)
    def get(self, id):
        """
        Returns a category with a list of posts.
        """
        return User.query.filter(User.id == id).one()

    @api.expect(user)
    @api.response(204, 'User successfully updated.')
    def put(self):
        """
        Updates the current User.
        Use this method to change the details of the current user.
        * Send a JSON object with the new details in the request body.
        ```
        {
          "firstname": "New Firstname",
          "lastname": "New Lastname"
          "email": "New Email",
          "password": "New Password"
        }
        ```
        """
        # data = request.json
        # update_user(get_current_user_id(), data)
        return None, 204

    @api.expect(user)
    @api.response(204, 'User successfully created.')
    def post(self):
        req_parse = reqparse.RequestParser(bundle_errors=True)
        req_parse.add_argument('email', type=str, required=True,
                               help='No email provided',
                               location='json')
        req_parse.add_argument('password', type=str, required=True,
                               help='No password provided',
                               location='json')
        req_parse.add_argument('firstname', type=str, required=True,
                               help='No first name provided',
                               location='json')
        req_parse.add_argument('lastname', type=str, required=True,
                               help='No last name provided',
                               location='json')

        args = req_parse.parse_args()

        email = args.get('email')
        firstname = args.get('firstname')
        lastname = args.get('lastname')
        password = args.get('password')

        if email == '':
            return {'message': {'email': 'No email provided'}}, 400
        elif not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
                          email):
            return {'message': {'email': 'Invalid email provided'}}, 400

        if password == '':
            return {'message': {'password': 'Invalid password provided'}}, 400
        elif len(password) < 8:
            return {
                'message': {
                    'password': 'Password must be at least 8 characters long'
                }
            }, 400

        if firstname == '':
            return {'message': {'firstname': 'No first name provided'}}, 400

        if lastname == '':
            return {'message': {'lastname': 'No last name provided'}}, 400

        new_user = User(email=email,
                        firstname=firstname,
                        lastname=lastname,
                        password=password)

        try:
            new_user.save()
        except IntegrityError:
            return {
                'description': 'User with given email already exists.'
            }, 409
        except Exception:
            return {'description': 'Server encountered an error.'}, 500

        return {'email': new_user.email}, 201
