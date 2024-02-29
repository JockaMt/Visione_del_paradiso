from functools import wraps
import sqlalchemy.exc
from api_vdp.src.model import Client, Room
from flask import session, redirect, url_for, render_template, request
from api_vdp.src.auth import cripto
from api_vdp.src.database import db


class Item:
    def create(self, name, description, size, data=None):
        item = {'name': name, 'description': description, 'size': size, 'data': data}
        return item

    def read(self, class_name):
        items = class_name.query.all()
        return items

    def update(self, id, class_name, item):
        result = class_name.get(id)
        result.name = item['name']
        result.description = item['description']
        result.size = item['size']
        result.data = item['data']
        return result

    def delete(self, id, class_name):
        room = class_name.query.get(id)
        if room:
            db.session.delete(room)
            db.session.commit()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


@login_required
def home_page():
    return render_template("home.html", client=session['user'], logged=True)


def login_page(app):
    db.create_all()
    if request.method == 'POST':
        email = request.form.get('m4il').strip()
        password = request.form.get('p4ss').strip()
        client = Client.query.filter_by(email=email).first()
        if client and client.encrypted_password == cripto(password, app.settings.SECRET_NUM):
            session['logged_in'] = True
            user = {'name': client.name, 'sex': client.sex, 'age': client.age, 'email': client.email,
                    'room': client.rooms, 'admin': client.admin}
            session['user'] = user
            return redirect(url_for("home"))
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")


def register_page(app):
    db.create_all()
    if request.method == 'POST':
        name = request.form.get('n4me').strip()
        email = request.form.get('m4il').strip()
        password = request.form.get('p4ss').strip()
        confirm_password = request.form.get('conf_p4ss').strip()
        if password == confirm_password:
            try:
                client = Client(
                    email=email,
                    encrypted_password=cripto(password, app.settings.SECRET_NUM),
                    name=name,
                    sex="Undefined",
                    age=0,
                    phone="",
                    admin=False
                )
                db.session.add(client)
                db.session.commit()
                return redirect(url_for("home"))
            except sqlalchemy.exc.IntegrityError as e:
                return render_template("register.html", msg="E-mail already registered!")
        else:
            return render_template("register.html", msg="Passwords not match!")
    else:
        return render_template("register.html")


@login_required
def edit_profile_page(app):
    if request.method == 'POST':
        name = request.form.get('n4me').strip()
        last_name = request.form.get('last-name').strip()
        email = request.form.get('m4il').strip()
        sex = request.form.get("sex").strip()
        age = request.form.get('age').strip()
        phone = request.form.get('phone').strip()
        try:
            if name and last_name and email and sex and age and phone:
                client = Client.query.filter_by(email=session['user']['email']).first()
                client.name = name
                client.last_name = last_name
                client.email = email
                client.age = age
                client.sex = sex
                client.phone = phone
                user = {'name': client.name,
                        'last_name': client.last_name,
                        'sex': client.sex,
                        'age': client.age,
                        'email': client.email,
                        'phone': client.phone,
                        'room': client.rooms,
                        'admin': client.admin
                        }
                session['user'] = user
                db.session.add(client)
                db.session.commit()
                return redirect(url_for("profile"))
            else:
                return redirect(url_for('edit_profile'))
        except:
            return redirect(url_for('edit_profile'))
    else:
        return render_template("edit-profile.html", user=session['user'], logged=True, form="profile")


@login_required
def rooms_page(app):
    _h = Item()
    rooms = _h.read(Room)
    print(rooms)
    return render_template("rooms.html", logged=True, rooms=rooms)


@login_required
def profile_page():
    client = Client.query.filter_by(email=session['user']['email']).first()
    user = {'name': client.name,
            'last_name': client.last_name,
            'sex': client.sex,
            'age': client.age,
            'email': client.email,
            'phone': client.phone,
            'room': client.rooms,
            'admin': client.admin
            }
    session['user'] = user
    return render_template('profile.html', user=session['user'], logged=True)


@login_required
def logout_page():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for("login"))


@login_required
def admin_page():
    if session['user']['admin']:
        return render_template('admin.html', user=session['user'], logged=True)
    return url_for('home')
