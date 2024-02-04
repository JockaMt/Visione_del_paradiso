from functools import wraps
from api_vdp.src.model import Client
from flask import session, redirect, url_for, render_template, request
from api_vdp.src.auth import cripto
from api_vdp.src.database import db

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@login_required
def home_page():
    lista = Client.query.all()
    return render_template("home.html", client=session['user'], logged=True)


def login_page(app):
    db.create_all()
    if request.method == 'POST':
        email = request.form.get('m4il')
        password = request.form.get('p4ss')
        client = Client.query.filter_by(email=email).first()
        if client and client.crypted_password == cripto(password, app.settings.SECRET_NUM):
            session['logged_in'] = True
            user = {'name': client.name, 'sex': client.sex, 'age': client.age, 'room': client.rooms}
            session['user'] = user
            return redirect(url_for("home"))
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")


def register_page(app):
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


@login_required
def profile_page():
    return render_template('profile.html', name=session['user']['name'], logged=True)


@login_required
def logout_page():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for("login"))