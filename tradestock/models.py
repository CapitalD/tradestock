from . import db

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return '<Job %r>' % (self.name)
