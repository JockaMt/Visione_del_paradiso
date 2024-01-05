from flask import render_template, request, url_for, redirect
from api_vdp.src.auth import cripto
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
            email = request.form.get('m4il')
            password = request.form.get('p4ss')
            client = Client.query.filter_by(email=email).first()
            if client and client.crypted_password == cripto(password, app.settings.SECRET_NUM):
                print(client)
                return redirect(url_for("home"))
            else:
                return render_template("login.html")
        else:
            return render_template("login.html")
        
    @app.route("/register", methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            name = request.form.get('n4me')
            email = request.form.get('m4il')
            password = request.form.get('p4ss')
            confirm_password = request.form.get('conf_p4ss')
            if password == confirm_password:
                try:
                    cliente = Client(
                        email=email, 
                        crypted_password=cripto(password, app.settings.SECRET_NUM), 
                        name=name,
                        sex="Undefined",
                        age=0,
                        room_id=None
                        )
                    db.session.add(cliente)
                    db.session.commit()
                    return redirect(url_for("home"))
                except:
                    return render_template("register.html", msg="E-mail already registered!")
            else:
                return render_template("register.html", msg="Passwords not match!")
        else:
            return render_template("register.html")