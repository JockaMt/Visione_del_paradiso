from flask import Flask
from .src import config

app = Flask(__name__)
config.init_app(app)
config.load_extensions(app)

if __name__ == '__main__':
    app.run(debug=True, port=5000)