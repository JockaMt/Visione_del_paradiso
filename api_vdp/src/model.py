from api_vdp.src.database import db

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clientes = db.relationship('Client', backref='room', lazy=True)
    size = db.Column(db.Integer)
    
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    crypted_password = db.Columns(db.Text)
    name = db.Column(db.String(80), nullable=False)
    sex = db.Column(db.String(16), nullable=True)
    age = db.Column(db.Integer)
    