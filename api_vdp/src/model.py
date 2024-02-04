from api_vdp.src.database import db

    
class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    crypted_password = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    sex = db.Column(db.String(16))
    age = db.Column(db.Integer)
    rooms = db.relationship('Room', back_populates='client')


class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.Integer)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    client = db.relationship('Client', back_populates='rooms')
