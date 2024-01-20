from dynaconf import FlaskDynaconf, settings

def init_app(app):
    FlaskDynaconf(app)
    app.settings = settings
    app.secret_key = app.settings.SECRET_KEY