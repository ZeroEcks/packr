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
    firstname = Column(db.String(30), nullable=True)
    lastname = Column(db.String(30), nullable=True)
    created_at = Column(db.DateTime,
                        nullable=False,
                        default=dt.datetime.utcnow)
    active = Column(db.Boolean(), default=True)
    business_account = db.Column(db.Boolean, nullable=True, default=False)
    role_id = Column(db.Integer(), db.ForeignKey('roles.id'))
    contact_id = Column(db.Integer(), db.ForeignKey('contacts.id'))

    role = relationship('Role', lazy='joined')
    contact = relationship('Contact', uselist=False)
    orders = db.relationship('Order', foreign_keys="Order.user_id")
    deliveries = db.relationship('Order', foreign_keys="Order.driver_id")
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
        return '<User({id})>'.format(id=self.id)


class ServiceType(SurrogatePK, Model):
    """A service type"""

    __tablename__ = 'service_types'
    name = Column(db.String(30), nullable=False)

    def __init__(self, **kwargs):
        """Create instance."""
        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<ServiceType({name})>'.format(name=self.name)


class DangerClass(SurrogatePK, Model):
    """A danger class"""

    __tablename__ = 'danger_classes'
    name = Column(db.String(30), nullable=False)

    def __init__(self, **kwargs):
        """Create instance."""
        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<DangerClass({name})>'.format(name=self.name)


class Address(SurrogatePK, Model):
    """An address"""

    __tablename__ = 'addresses'
    street = Column(db.String(80), nullable=False)
    suburb = Column(db.String(30), nullable=False)
    state = Column(db.String(15), nullable=False)
    post_code = Column(db.Integer, nullable=False)

    def __init__(self, **kwargs):
        """Create instance."""
        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Address({street})>'.format(street=self.street)


class Contact(SurrogatePK, Model):
    """A contact"""

    __tablename__ = 'contacts'
    business_name = Column(db.String(80), nullable=False)
    contact_name = Column(db.String(40), nullable=False)
    phone = Column(db.String(20), nullable=False)
    email = Column(db.String(80), nullable=False)

    def __init__(self, **kwargs):
        """Create instance."""
        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Contact({id})>'.format(id=self.id)


class Order(SurrogatePK, Model):
    """An order."""

    __tablename__ = 'orders'
    created_at = Column(db.DateTime,
                        nullable=False,
                        default=dt.datetime.utcnow)
    weight = Column(db.Float(), nullable=False)
    notes = Column(db.Text, nullable=True)
    driver_notes = Column(db.Text, nullable=True)
    cost = Column(db.Float, nullable=False)
    eta = Column(db.Date, nullable=True)
    pickup_time = Column(db.DateTime,
                         nullable=False,
                         default=dt.datetime.utcnow)
    fragile = Column(db.Boolean(), nullable=False)
    payment_type = Column(db.String(20), nullable=False)
    user_id = Column(db.Integer, db.ForeignKey('users.id'))
    driver_id = Column(db.Integer, db.ForeignKey('users.id'))
    delivery_address_id = Column(db.Integer, db.ForeignKey('addresses.id'))
    delivery_contact_id = Column(db.Integer, db.ForeignKey('contacts.id'))
    pickup_address_id = Column(db.Integer, db.ForeignKey('addresses.id'))
    pickup_contact_id = Column(db.Integer, db.ForeignKey('contacts.id'))
    danger_id = Column(db.Integer(), db.ForeignKey('danger_classes.id'))
    service_type_id = Column(db.Integer(), db.ForeignKey('service_types.id'))

    danger = relationship('DangerClass', uselist=False)
    payment = relationship("Payment",
                           backref=db.backref("order", uselist=False))
    package = relationship("Package", backref="order")
    status = relationship("OrderStatus", backref='order')
    delivery = relationship("Delivery", backref='order')
    issue = relationship("Issue", backref='order')
    driver = relationship("User",
                          uselist=False,
                          foreign_keys="Order.driver_id")
    user = relationship("User",
                        uselist=False,
                        foreign_keys="Order.user_id")
    delivery_address = relationship('Address',
                                    uselist=False,
                                    foreign_keys="Order.delivery_address_id")
    pickup_address = relationship('Address',
                                  uselist=False,
                                  foreign_keys="Order.pickup_address_id")
    delivery_contact = relationship('Contact',
                                    uselist=False,
                                    foreign_keys="Order.delivery_contact_id")
    pickup_contact = relationship('Contact',
                                  uselist=False,
                                  foreign_keys="Order.pickup_contact_id")
    service_type = relationship('ServiceType',
                                uselist=False,
                                foreign_keys="Order.service_type_id")

    def __init__(self, **kwargs):
        """Create instance."""
        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Order({id})>'.format(id=self.id)


class StatusType(SurrogatePK, Model):
    """A type of status."""

    __tablename__ = 'status_types'
    name = Column(db.String(10), nullable=False)
    status = Column(db.String(80), nullable=False)

    def __init__(self, **kwargs):
        """Create instance."""
        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<StatusType({name})>'.format(name=self.name)


class OrderStatus(SurrogatePK, Model):
    """A status for an order."""

    __tablename__ = 'order_statuses'
    time = Column(db.DateTime, nullable=False)
    address = Column(db.String(80), nullable=False)
    order_id = Column(db.Integer, db.ForeignKey('orders.id'))
    status_id = Column(db.Integer, db.ForeignKey('status_types.id'))

    status = relationship('StatusType', uselist=False)

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
    width = Column(db.Float(), nullable=False)
    height = Column(db.Float(), nullable=False)
    length = Column(db.Float(), nullable=False)
    order_id = Column(db.Integer, db.ForeignKey('orders.id'))
    delivery_id = Column(db.Integer, db.ForeignKey('deliveries.id'))

    def __init__(self, **kwargs):
        """Create instance."""
        db.Model.__init__(self, **kwargs)

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
