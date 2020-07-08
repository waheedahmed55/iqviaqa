from . import db
from . import app
from flask_marshmallow import Marshmallow
ma = Marshmallow(app)


class Message(db.Model):
    # Defining the message model, which contains content to be display and datetime of when its to be displayed
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    time = db.Column(db.DateTime)

    # Defining save method to add records to database
    def save(self):
        db.session.add(self)
        db.session.commit()

    # Defining remove methos to remove records from database
    def delete(self):
        db.session.delete(self)
        db.session.commit()


class MessageSchema(ma.Schema):
    # Defining the schema used to return JSON response
    class Meta:
        fields = ("id", "content", "time")
