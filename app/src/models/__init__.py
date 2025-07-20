from ..database import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avatar = db.Column(
        db.String(200),
        nullable=True,
        default="https://placehold.co/500x400?text=Avatar",
    )
    hash_password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), default="Undefined")
    sex = db.Column(db.String(16), default="Undefined")
    age = db.Column(db.Integer)
    phone = db.Column(db.String(120))
    admin = db.Column(db.Boolean, default=False)

    rooms = db.relationship(
        "Rooms", back_populates="user", cascade="all, delete-orphan"
    )
    user_events = db.relationship("UserEvent", back_populates="user", cascade="all, delete-orphan")
    events = db.relationship("Events", secondary="user_events", viewonly=True)

    user_services = db.relationship("UserService", back_populates="user", cascade="all, delete-orphan")
    services = db.relationship("Services", secondary="user_services", viewonly=True)

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
    image = db.Column(
        db.String(200),
        nullable=True,
        default="https://images.pexels.com/photos/19836801/pexels-photo-19836801.jpeg",
    )
    price = db.Column(db.Float, nullable=False, default=0.0)
    capacity = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    user = db.relationship("User", back_populates="rooms")

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
    
    @classmethod
    def is_occupied(cls, room_id):
        room = Rooms.get_by_id(room_id)
        if room:
            return bool(room.user_id)  # Verifica se o quarto tem um usuário associado
        return False


class Events(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    user_events = db.relationship("UserEvent", back_populates="event", cascade="all, delete-orphan")
    users = db.relationship("User", secondary="user_events", viewonly=True)

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
    image = db.Column(
        db.String(255),
        nullable=True,
        default="https://img.freepik.com/fotos-gratis/rotina-domestica-dona-de-casa-sorridente-em-pe-de-avental-na-cozinha_259150-59700.jpg",
    )
    description = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    user_services = db.relationship("UserService", back_populates="service", cascade="all, delete-orphan")
    users = db.relationship("User", secondary="user_services", viewonly=True)

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
    def update(cls, identifier, by_username=True, **kwargs):
        if by_username:
            user = db.session.query(cls).filter_by(username=identifier).first()
        else:
            user = db.session.query(cls).filter_by(id=identifier).first()
        
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            db.session.commit()
            return user
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

class UserEvent(db.Model):
    __tablename__ = "user_events"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), primary_key=True)

    user = db.relationship("User", back_populates="user_events")
    event = db.relationship("Events", back_populates="user_events")
    
    @classmethod
    def get_by_user_and_event(cls, user_id, event_id):
        return db.session.query(cls).filter_by(user_id=user_id, event_id=event_id).first()
    
    @classmethod
    def create(cls, user_id, event_id):
        user_event = cls(user_id=user_id, event_id=event_id)
        db.session.add(user_event)
        db.session.commit()
        return user_event
    
    @classmethod
    def delete(cls, user_id, event_id):
        user_event = db.session.query(cls).filter_by(user_id=user_id, event_id=event_id).first()
        if user_event:
            db.session.delete(user_event)
            db.session.commit()
            return True
        return False
    
    @classmethod
    def find_by_user_and_event(cls, user_id, event_id):
        return db.session.query(cls).filter_by(user_id=user_id, event_id=event_id).first()


class UserService(db.Model):
    __tablename__ = "user_services"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), primary_key=True)

    user = db.relationship("User", back_populates="user_services")
    service = db.relationship("Services", back_populates="user_services")
    
    @classmethod
    def get_by_user_and_service(cls, user_id, service_id):
        return db.session.query(cls).filter_by(user_id=user_id, service_id=service_id).first()
    
    @classmethod
    def create(cls, user_id, service_id):
        user_service = cls(user_id=user_id, service_id=service_id)
        db.session.add(user_service)
        db.session.commit()
        return user_service
    
    @classmethod
    def delete(cls, user_id, service_id):
        user_service = db.session.query(cls).filter_by(user_id=user_id, service_id=service_id).first()
        if user_service:
            db.session.delete(user_service)
            db.session.commit()
            return True
        return False
    
    @classmethod
    def find_by_user_and_service(cls, user_id, service_id):
        return db.session.query(cls).filter_by(user_id=user_id, service_id=service_id).first()

def search_by_name(cls, termo: str):
    termo = termo.strip().lower()
    return (
        db.session.query(cls).filter(db.func.lower(cls.name).like(f"%{termo}%")).all()
    )

def get_room_owner(room_id: int):
    room = Rooms.get_by_id(room_id)
    if room and room.user:
        return room.user.username
    return None

def search_by_name_with_user(cls, termo: str, username: str):
    termo = f"%{termo.strip().lower()}%"
    return (
        db.session.query(cls)
        .join(User, cls.user_id == User.id)
        .filter(db.func.lower(cls.name).like(termo), User.username == username)
        .all()
    )
    
def search_service_by_name_with_user_from_relation(termo: str, username: str):
    termo = f"%{termo.strip().lower()}%"
    return (
        db.session.query(Services)
        .join(UserService, Services.id == UserService.service_id)
        .join(User, UserService.user_id == User.id)
        .filter(db.func.lower(Services.name).like(termo), User.username == username)
        .all()
    )
    
def search_event_by_name_with_user_from_relation(termo: str, username: str):
    termo = f"%{termo.strip().lower()}%"
    return (
        db.session.query(Events)
        .join(UserEvent, Events.id == UserEvent.event_id)
        .join(User, UserEvent.user_id == User.id)
        .filter(db.func.lower(Events.name).like(termo), User.username == username)
        .all()
    )