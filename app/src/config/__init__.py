from dynaconf import FlaskDynaconf, settings

def init_app(app):
    FlaskDynaconf(app)
    app.settings = settings
    app.secret_key = app.settings.SECRET_KEY
    
def load_extensions(app):
    for extension in app.settings.EXTENSIONS:
        module = __import__(extension, fromlist=['init_app'])
        module.init_app(app)

    return app