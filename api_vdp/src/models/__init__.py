from ..database import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), default="Undefined")
    sex = db.Column(db.String(16), default="Undefined")
    age = db.Column(db.Integer)
    phone = db.Column(db.String(120))
    admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.username}>'

    @classmethod
    def create(cls, username, email, name, last_name="Undefined", sex="Undefined", age=None, phone=None, admin=False):
        db.create_all()  # geralmente é melhor fazer isso fora da lógica de negócio
        user = cls(
            username=username,
            email=email,
            name=name,
            last_name=last_name,
            sex=sex,
            age=age,
            phone=phone,
            admin=admin
        )
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def exists(cls, username):
        return db.session.query(cls).filter_by(username=username).first() is not None

    @classmethod
    def list_all(cls):
        return db.session.query(cls).all()
