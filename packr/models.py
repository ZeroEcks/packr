# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from packr.database import Column, Model, SurrogatePK, db, relationship
from packr.extensions import bcrypt


class Role(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = 'roles'
    role_name = Column(db.String(80), unique=True, nullable=False)

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.role_name)


class User(SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    email = Column(db.String(80), unique=True, nullable=False)
    password = Column(db.String(128), nullable=True)
    created_at = Column(db.DateTime,
                        nullable=False,
                        default=dt.datetime.utcnow)
    firstname = Column(db.String(30), nullable=True)
    lastname = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=True)
    business_account = db.Column(db.Boolean, nullable=True, default=False)
    role_id = Column(db.Integer(), db.ForeignKey('roles.id'))
    role = relationship('Role', lazy='joined')

    orders = db.relationship('Order', backref='user')
    conversations = relationship('Conversation', backref='user', lazy='joined')

    def __init__(self, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self,
                          email=email,
                          **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def verify_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return '{0} {1}'.format(self.firstname, self.lastname)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)


# Due to a limitation in SQLAlchemy, we can't use a User for this.
class Driver(SurrogatePK, Model):
    """A driver for the company."""

    __tablename__ = 'drivers'
    email = Column(db.String(80), unique=True, nullable=False)
    password = Column(db.String(128), nullable=True)
    created_at = Column(db.DateTime,
                        nullable=False,
                        default=dt.datetime.utcnow)
    firstname = Column(db.String(30), nullable=True)
    lastname = Column(db.String(30), nullable=True)

    orders = db.relationship('Order', backref='driver')

    def __init__(self, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self,
                          email=email,
                          **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def verify_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return '{0} {1}'.format(self.firstname, self.lastname)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Driver({full_name})>'.format(
            full_name='{0} {1}'.format(self.firstname, self.lastname))


class Address(SurrogatePK, Model):
    """An address"""

    __tablename__ = 'addresses'
    street = Column(db.String(80), nullable=False)
    suburb = Column(db.String(30), nullable=False)
    state = Column(db.String(15), nullable=False)
    post_code = Column(db.Integer, nullable=False)
    order_id = Column(db.Integer, db.ForeignKey('orders.id'))

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Address({street})>'.format(street=self.street)


class Order(SurrogatePK, Model):
    """An order."""

    __tablename__ = 'orders'
    created_at = Column(db.DateTime,
                        nullable=False,
                        default=dt.datetime.utcnow)
    weight = Column(db.Float(), nullable=False)
    details = Column(db.Text, nullable=True)
    notes = Column(db.Text, nullable=True)
    driver_notes = Column(db.Text, nullable=True)
    cost = Column(db.Float, nullable=False)
    eta = Column(db.Date, nullable=True)
    user_id = Column(db.Integer, db.ForeignKey('users.id'))
    driver_id = Column(db.Integer, db.ForeignKey('drivers.id'))
    delivery_address_id = Column(db.Integer, db.ForeignKey('addresses.id'))
    pickup_address_id = Column(db.Integer, db.ForeignKey('addresses.id'))

    payment = relationship("Payment",
                           backref=db.backref("order", uselist=False))
    package = relationship("Package", backref="order")
    status = relationship("OrderStatus", backref='order')
    delivery = relationship("Delivery", backref='order')
    issue = relationship("Issue", backref='order')
    delivery_address = relationship('Address',
                                    uselist=False,
                                    foreign_keys="Order.delivery_address_id")
    pickup_address = relationship('Address',
                                  uselist=False,
                                  foreign_keys="Order.pickup_address_id")

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Order({id})>'.format(id=self.id)


class OrderStatus(SurrogatePK, Model):
    """A status for an order."""

    __tablename__ = 'order_statuses'
    status = Column(db.String(80), nullable=False)
    time = Column(db.DateTime, nullable=False)
    address = Column(db.String(80), nullable=False)
    order_id = Column(db.Integer, db.ForeignKey('orders.id'))

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<OrderStatus({status}, {time})>'.format(status=self.status,
                                                        time=self.time)


class Delivery(SurrogatePK, Model):
    """A delivery for an order."""

    __tablename__ = 'deliveries'
    order_id = Column(db.Integer, db.ForeignKey('orders.id'))
    driver_notes = Column(db.Text, nullable=True)
    signature = Column(db.Boolean, nullable=False, default=False)
    type_id = Column(db.Integer, db.ForeignKey('delivery_types.id'))

    package = relationship("Package", backref="delivery")
    delivery_type = relationship("DeliveryType", uselist=False)

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Delivery({id})>'.format(id=self.id)


class DeliveryType(SurrogatePK, Model):
    """A type for a delivery."""

    __tablename__ = "delivery_types"
    # Can't call it name due to table name stored as name
    type_name = Column(db.String(12), nullable=False)

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<DeliveryType({name})>'.format(name=self.type_name)


class Issue(SurrogatePK, Model):
    """An issue for an order."""

    __tablename__ = "issues"
    # Can't call it name due to table name stored as name
    issue = Column(db.Text, nullable=False)
    order_id = Column(db.Integer, db.ForeignKey('orders.id'))

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Issue({issue})>'.format(issue=self.issue)


class Payment(SurrogatePK, Model):
    """A payment for an order."""

    __tablename__ = "payments"
    stripe_id = Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Payment({id}, {stripe_id})>'.format(id=self.id,
                                                     stripe_id=self.stripe_id)


class Package(SurrogatePK, Model):
    """A package for an order."""

    __tablename__ = "packages"
    weight = Column(db.Float(), nullable=False)
    dimensions = Column(db.String(32), nullable=False)
    danger_class = Column(db.Integer(), nullable=False, default=0)
    fragile = Column(db.Boolean(), nullable=False)
    order_id = Column(db.Integer, db.ForeignKey('orders.id'))
    delivery_id = Column(db.Integer, db.ForeignKey('deliveries.id'))

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Package({id})>'.format(id=self.id)


class Conversation(SurrogatePK, Model):
    """A conversation for a user"""

    __tablename__ = "conversations"
    user_id = Column(db.Integer, db.ForeignKey('users.id'))

    messages = relationship('Message', backref='conversation')

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Conversation({id})>'.format(id=self.id)


class Message(SurrogatePK, Model):
    """A message for a conversation"""

    __tablename__ = "messages"
    content = Column(db.Text, nullable=False)
    time = Column(db.Time(), nullable=False)

    conversation_id = Column(db.Integer, db.ForeignKey('conversations.id'))

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Message({id})>'.format(id=self.id)
