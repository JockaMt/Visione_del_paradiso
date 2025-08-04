from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        # You can add more initialization logic here if needed
        # For example, creating default users or roles
        # db.session.add(User(username='admin',