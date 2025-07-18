from ..database import db


def search_by_name(cls, termo: str):
    termo = termo.strip().lower()
    return db.session.query(cls).filter(db.func.lower(cls.name).like(f"%{termo}%")).all()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hash_password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), default="Undefined")
    sex = db.Column(db.String(16), default="Undefined")
    age = db.Column(db.Integer)
    phone = db.Column(db.String(120))
    admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User {self.username}>"

    @classmethod
    def create(
        cls,
        username,
        email,
        name,
        hash_password,
        last_name="Undefined",
        sex="Undefined",
        age=None,
        phone=None,
        admin=False,
    ):
        db.create_all()  # geralmente é melhor fazer isso fora da lógica de negócio
        user = cls(
            username=username,
            email=email,
            hash_password=hash_password,  # Use a secure hash function
            name=name,
            last_name=last_name,
            sex=sex,
            age=age,
            phone=phone,
            admin=admin,
        )
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def exists(cls, username):
        return db.session.query(cls).filter_by(username=username).first() is not None

    @classmethod
    def delete(cls, username):
        user = db.session.query(cls).filter_by(username=username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False

    @classmethod
    def update(cls, username, **kwargs):
        user = db.session.query(cls).filter_by(username=username).first()
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            db.session.commit()
            return user
        return None

    @classmethod
    def get_by_username(cls, username):
        return db.session.query(cls).filter_by(username=username).first()

    @classmethod
    def list_all(cls):
        return db.session.query(cls).all()


class Rooms(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    image = db.Column(db.String(200), nullable=True, default="https://images.pexels.com/photos/19836801/pexels-photo-19836801.jpeg")
    price = db.Column(db.Float, nullable=False, default=0.0)
    capacity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Room {self.name}>"

    @classmethod
    def create(cls, name, description=None, capacity=0):
        room = cls(name=name, description=description, capacity=capacity)
        db.session.add(room)
        db.session.commit()
        return room

    @classmethod
    def list_all(cls):
        return db.session.query(cls).all()

    @classmethod
    def get_by_id(cls, room_id):
        return db.session.query(cls).filter_by(id=room_id).first()

    @classmethod
    def update(cls, room_id, **kwargs):
        room = db.session.query(cls).filter_by(id=room_id).first()
        if room:
            for key, value in kwargs.items():
                setattr(room, key, value)
            db.session.commit()
            return room
        return None

    @classmethod
    def delete(cls, room_id):
        room = db.session.query(cls).filter_by(id=room_id).first()
        if room:
            db.session.delete(room)
            db.session.commit()
            return True
        return False

    @classmethod
    def exists(cls, name):
        return db.session.query(cls).filter_by(name=name).first() is not None


class Events(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Event {self.name}>"

    @classmethod
    def create(cls, name, description=None, date=None, room_id=None):
        event = cls(name=name, description=description, date=date, room_id=room_id)
        db.session.add(event)
        db.session.commit()
        return event

    @classmethod
    def list_all(cls):
        return db.session.query(cls).all()

    @classmethod
    def get_by_id(cls, event_id):
        return db.session.query(cls).filter_by(id=event_id).first()

    @classmethod
    def update(cls, event_id, **kwargs):
        event = db.session.query(cls).filter_by(id=event_id).first()
        if event:
            for key, value in kwargs.items():
                setattr(event, key, value)
            db.session.commit()
            return event
        return None

    @classmethod
    def delete(cls, event_id):
        event = db.session.query(cls).filter_by(id=event_id).first()
        if event:
            db.session.delete(event)
            db.session.commit()
            return True
        return False

    @classmethod
    def exists(cls, name):
        return db.session.query(cls).filter_by(name=name).first() is not None


class Services(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Service {self.name}>"

    @classmethod
    def create(cls, name, description=None, price=0.0):
        service = cls(name=name, description=description, price=price)
        db.session.add(service)
        db.session.commit()
        return service

    @classmethod
    def list_all(cls):
        return db.session.query(cls).all()

    @classmethod
    def get_by_id(cls, service_id):
        return db.session.query(cls).filter_by(id=service_id).first()

    @classmethod
    def update(cls, service_id, **kwargs):
        service = db.session.query(cls).filter_by(id=service_id).first()
        if service:
            for key, value in kwargs.items():
                setattr(service, key, value)
            db.session.commit()
            return service
        return None

    @classmethod
    def delete(cls, service_id):
        service = db.session.query(cls).filter_by(id=service_id).first()
        if service:
            db.session.delete(service)
            db.session.commit()
            return True
        return False

    @classmethod
    def exists(cls, name):
        return db.session.query(cls).filter_by(name=name).first() is not None
