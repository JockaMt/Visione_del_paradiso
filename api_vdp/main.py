from flask import Flask
from api_vdp.src import views, database, config, admin_controller

app = Flask(__name__)
config.init_app(app)
views.init_app(app)
admin_controller.init_app(app)
database.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
