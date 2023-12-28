from flask import render_template, url_for

def init_app(app):
    @app.route("/")
    def home():
        return render_template("home.html", name="Hello World")
    
    @app.route("/login")
    def login():
        return render_template("login.html")