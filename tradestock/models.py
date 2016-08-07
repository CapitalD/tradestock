from . import db

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return '<Job %r>' % (self.name)

class Stockitem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(255))
    name = db.Column(db.String(255), nullable=False)
    unitprice = db.Column(db.Float)
    quantity = db.Column(db.Float)

    def __repr__(self):
        return '<Stockitem %r>' % (self.name)
