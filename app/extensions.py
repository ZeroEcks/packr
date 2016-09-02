from flask_bcrypt import Bcrypt
from flask_jwt import JWT
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

api = Api()
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWT()
