from flask import Flask
from .src import views, database, config
import logging

app = Flask(__name__)
config.init_app(app)
views.init_app(app)
database.init_app(app)

logging.basicConfig(level=logging.DEBUG)
logging.debug("Starting the application...")

if __name__ == '__main__':
    app.run(debug=True, port=8080)