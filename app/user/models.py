from app.core.models import CreatedAtMixin, CRUDMixin, IdMixin
from app.extensions import bcrypt, db


# from app.order.models import Order


class User(CreatedAtMixin, CRUDMixin, IdMixin, db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String(200), unique=True, nullable=False)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    business_account = db.Column(db.Boolean, nullable=True, default=False)
    admin_account = db.Column(db.Boolean, nullable=True, default=False)

    orders = db.relationship('Order', backref='user', lazy='joined')

    def __init__(self, email, firstname, lastname, password,
                 business_account=False, admin_account=False):
        super().__init__()

        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.firstname = firstname
        self.lastname = lastname
        self.business_account = business_account
        self.admin_account = admin_account

    def __repr__(self):
        return '<User {0}>'.format(self.email)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
