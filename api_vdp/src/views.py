from flask import render_template, request, url_for, redirect
from api_vdp.src.database import db
from api_vdp.src.model import Client

def init_app(app):
    @app.route("/")
    def home():
        db.create_all()
        lista = Client.query.all()
        return render_template("home.html", lista=lista)
    
    @app.route("/login", methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            return redirect(url_for("home"))
        else:
            return render_template("login.html")