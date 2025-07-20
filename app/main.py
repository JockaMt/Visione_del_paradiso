from flask import Flask
# from flask_migrate import Migrate
from .src.database import db
from .src import config

app = Flask(__name__)
config.init_app(app)
config.load_extensions(app)

# migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True, port=5000)