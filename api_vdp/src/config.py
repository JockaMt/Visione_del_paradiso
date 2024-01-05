from dynaconf import FlaskDynaconf, settings

def init_app(app):
    FlaskDynaconf(app)
    app.settings = settings