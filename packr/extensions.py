# -*- coding: utf-8 -*-
"""
Extensions module.
Each extension is initialized in the app factory located in app.py.
"""
from flask_bcrypt import Bcrypt
from flask_cache import Cache
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT

bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
jwt = JWT()
