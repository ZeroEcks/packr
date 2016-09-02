from app.core.models import CreatedAtMixin, CRUDMixin, IdMixin
from app.extensions import db


class Order(CreatedAtMixin, CRUDMixin, IdMixin, db.Model):
    __tablename__ = 'order'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self):
        super().__init__()

    def __repr__(self):
        return '<Order {0}>'.format(self.id)
