import re
from datetime import datetime

from flask import current_app as app
from flask_jwt import current_identity
from flask_restplus import Namespace, Resource, fields, reqparse
from sqlalchemy.exc import IntegrityError

from packr.models import Message

api = Namespace('contact',
                description='Operations related to the contact form')

message = api.model('Contact', {
    'email': fields.String(required=True,
                           description='Contact email'),
    'content': fields.String(required=True,
                             description='Message'),
})

message_id = api.model('ContactCompletion', {
    'id': fields.Integer(required=True,
                         description='id')
})


@api.route('/')
class MessageItem(Resource):
    @api.expect(message)
    @api.response(204, 'Message successfully received.')
    def post(self):
        req_parse = reqparse.RequestParser(bundle_errors=True)
        req_parse.add_argument('email', type=str, required=True,
                               help='No email provided',
                               location='json')
        req_parse.add_argument('content', type=str, required=True,
                               help='No message provided',
                               location='json')

        args = req_parse.parse_args()

        email = args.get('email')
        content = args.get('content')

        if email == '':
            return {'message': {'email': 'No email provided'}}, 400
        elif not re.match(r"^[A-Za-z0-9.+_-]+@[A-Za-z0-9._-]+\.[a-zA-Z]*$",
                          email):
            return {'message': {'email': 'Invalid email provided'}}, 400

        if content == '':
            return {'message': {'content': 'No content provided'}}, 400

        new_message = Message(email=email,
                              content=content,
                              time=datetime.now())

        try:
            new_message.save()
        except IntegrityError as e:
            print(e)
            return {
                       'description': 'Failed to send message.'
                   }, 409
        except Exception as e:
            print(e)
            return {'description': 'Server encountered an error.'}, 500

        return {'email': new_message.email}, 201

    def get(self):
        if not current_identity and not app.config.get('TESTING'):
            return {'message': 'User not authenticated'}, 401
        if app.config.get('TESTING') \
                or current_identity.role.role_name == "ADMIN":
            messages = dict()
            for message_row in Message.query.filter_by(done=False).all():
                messages[message_row.id] = {
                    "email": message_row.email,
                    "time": message_row.time.isoformat(),
                    "content": message_row.content
                }
            return messages, 201
        else:
            return {'message': 'Not authorised'}, 401


@api.route('/complete')
class CompleteItem(Resource):
    @api.expect(message_id)
    @api.response(204, 'Message successfully updated.')
    def post(self):
        req_parse = reqparse.RequestParser(bundle_errors=True)
        req_parse.add_argument('id', type=int, required=True,
                               help='No id provided',
                               location='json')

        args = req_parse.parse_args()

        id = args.get('id')

        if id == 0:
            return {'message': {'id': 'No id provided'}}, 400

        completed_message = Message.query.filter_by(id=id).first()
        completed_message.done = True

        try:
            completed_message.save()
        except IntegrityError as e:
            print(e)
            return {
                       'description': 'Failed to update message.'
                   }, 409
        except Exception as e:
            print(e)
            return {'description': 'Server encountered an error.'}, 500

        return {'message': "Message updated"}, 201
