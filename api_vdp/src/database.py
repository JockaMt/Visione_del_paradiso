from flask_sqlalchemy import SQLAlchemy

def init_app(app):
    db = SQLAlchemy(app)
