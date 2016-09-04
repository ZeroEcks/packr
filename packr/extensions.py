# -*- coding: utf-8 -*-
"""
Extensions module.
Each extension is initialized in the app factory located in app.py.
"""
from flask_bcrypt import Bcrypt
from flask_cache import Cache
from flask_jwt import JWT
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
jwt = JWT()
