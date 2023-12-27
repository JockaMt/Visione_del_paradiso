from flask import render_template, url_for

def init_app(app):
    @app.route("/")
    def home():
        return render_template("home/index.html", name="Hello World")