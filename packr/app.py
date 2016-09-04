# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask

from datetime import datetime
from packr.models import User
from packr.api import blueprint as api
from packr.extensions import bcrypt, cache, db, migrate, jwt # noqa
from packr.settings import ProdConfig, Config


def create_app(config_object=ProdConfig):
    """An application factory.
    http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.authentication_handler(authenticate)
    jwt.identity_handler(identity)
    jwt.jwt_payload_handler(payload_handler)
    jwt.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    from packr.home.views import home
    app.register_blueprint(api, url_prefix='/api/')
    # app.register_blueprint(home)
    return None


def authenticate(email, password):
    user = User.query.filter_by(email=email).first()

    if not user or not user.verify_password(password):
        return None

    return user


def identity(payload):
    user_id = payload['identity']
    user = User.query.get(user_id)

    if not user:
        return None

    return user


def payload_handler(identity):
    iat = datetime.utcnow()
    exp = iat + Config.JWT_EXPIRATION_DELTA
    nbf = iat + Config.JWT_NOT_BEFORE_DELTA
    identity_id = getattr(identity, 'id') or identity['id']
    identity_firstname = (getattr(identity, 'firstname')
                          or identity['firstname'])
    return {
        'exp': exp,
        'iat': iat,
        'nbf': nbf,
        'identity': identity_id,
        'firstname': identity_firstname
    }
