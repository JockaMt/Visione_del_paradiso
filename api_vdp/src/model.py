from api_vdp.src.database import db


class Client_event(db.Model):
    __tablename__ = 'client_event'
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)


class Client_service(db.Model):
    __tablename__ = 'client_service'
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), primary_key=True)


class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    encrypted_password = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), default="Undefined")
    sex = db.Column(db.String(16), default="Undefined")
    age = db.Column(db.Integer)
    phone = db.Column(db.String(120))
    admin = db.Column(db.Boolean, default=False)
    rooms = db.relationship('Room', back_populates='client')
    events = db.relationship('Event', secondary='client_event', back_populates='clients')
    services = db.relationship('Service', secondary='client_service', back_populates='clients')


class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    size = db.Column(db.Integer)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    client = db.relationship('Client', back_populates='rooms')


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    size = db.Column(db.Integer)
    date = db.Column(db.DateTime, nullable=False)
    clients = db.relationship('Client', secondary='client_event', back_populates='events')


class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    size = db.Column(db.Integer)
    date = db.Column(db.DateTime, nullable=False)
    clients = db.relationship('Client', secondary='client_service', back_populates='services')


db.ForeignKeyConstraint([Client_event.client_id], [Client.id])
db.ForeignKeyConstraint([Client_event.event_id], [Event.id])
db.ForeignKeyConstraint([Client_service.client_id], [Client.id])
db.ForeignKeyConstraint([Client_service.service_id], [Service.id])
