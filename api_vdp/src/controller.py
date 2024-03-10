from api_vdp.src.auth import login_required
import sqlalchemy.exc
from api_vdp.src.model import Client, Room, Event, Service, Item, Client_event, Client_service
from flask import session, redirect, url_for, render_template, request
from api_vdp.src.auth import cripto
from api_vdp.src.database import db


def go_home(message=None):
    if session['logged_in']:
        if message:
            session['message'] = message
        return redirect(url_for('home'))


@login_required
def home_page():
    room = Room.query.first()
    return render_template("home.html", client=session['user'], logged=True, destaque=room)


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
            return go_home()
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")


def register_page(app):
    db.create_all()
    if request.method == 'POST':
        name = request.form.get('n4me').strip().capitalize()
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
                session['logged_in'] = True
                user = {'name': client.name, 'sex': client.sex, 'age': client.age, 'email': client.email,
                        'room': client.rooms, 'admin': client.admin}
                session['user'] = user
                db.session.add(client)
                db.session.commit()
                return go_home("User registered successfully!")
            except sqlalchemy.exc.IntegrityError as _:
                return render_template("register.html", msg="E-mail already registered!")
        else:
            return render_template("register.html", msg="Passwords not match!")
    else:
        return render_template("register.html")


@login_required
def edit_profile_page():
    if request.method == 'POST':
        name = request.form.get('n4me').strip().capitalize()
        last_name = request.form.get('last-name').strip().capitalize()
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
                user = {'id': client.id,
                        'name': client.name,
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
        except sqlalchemy.exc.IntegrityError as _:
            return redirect(url_for('edit_profile'))
    else:
        return render_template("edit-profile.html", user=session['user'], logged=True, form="profile")


@login_required
def profile_page():
    client = Client.query.filter_by(email=session['user']['email']).first()
    user = {'id': client.id,
            'name': client.name,
            'last_name': client.last_name,
            'sex': client.sex,
            'age': client.age,
            'email': client.email,
            'phone': client.phone,
            'admin': client.admin
            }
    rooms = Room.query.filter_by(client_id=client.id).count()
    events = Client_event.query.filter_by(client_id=client.id).count()
    services = Client_service.query.filter_by(client_id=client.id).count()
    session['items'] = {'rooms': rooms, 'events': events, 'services': services}
    session['user'] = user
    return render_template('profile.html', user=session['user'], items=session['items'], logged=True)


@login_required
def rooms_page():
    _h = Item()
    rooms = _h.read(Room)
    info = {'title': "Rooms", 'items': rooms}
    return render_template("catalog.html", logged=True, info=info)


@login_required
def my_rooms_page():
    client = Client.query.filter_by(email=session['user']['email']).first()
    rooms = Room.query.filter_by(client_id=client.id).all()
    info = {'title': "My rooms", 'items': rooms}
    return render_template("catalog.html", logged=True, info=info)


@login_required
def events_page():
    client = Client.query.filter_by(email=session['user']['email']).first()
    events = Client_event.query.filter_by(client_id=client.id)
    aux = []
    for event in events:
        aux.append(Event.query.filter_by(id=event.event_id).first())
    info = {'title': "Events", 'items': aux}
    return render_template('catalog.html', user=session['user'], logged=True, info=info)


@login_required
def my_events_page():
    _h = Item()
    events = _h.read(Event)
    info = {'title': "Events", 'items': events}
    return render_template('catalog.html', user=session['user'], logged=True, info=info)


@login_required
def services_page():
    client = Client.query.filter_by(email=session['user']['email']).first()
    services = Client_service.query.filter_by(client_id=client.id)
    aux = []
    for service in services:
        aux.append(Service.query.filter_by(id=service.service_id).first())
    info = {'title': "Services", 'items': aux}
    return render_template('catalog.html', user=session['user'], logged=True, info=info)


@login_required
def my_services_page():
    _h = Item()
    services = _h.read(Service)
    info = {'title': "Services", 'items': services}
    return render_template('catalog.html', user=session['user'], logged=True, info=info)


@login_required
def rate_us_page():
    return render_template('rate_us.html', user=session['user'], logged=True)


def support_page():
    return render_template('support.html')


@login_required
def catalog_item(class_id, class_name):
    _h = Item()
    item = None
    client_id = Client.query.filter_by(email=session['user']['email']).first().id
    match class_name:
        case "Room":
            item = _h.view(class_id, Room)
            if request.method == 'POST':
                if item.client_id == client_id:
                    item.client_id = None
                else:
                    item.client_id = client_id
                db.session.add(item)
                db.session.commit()
                return redirect(url_for("rooms"))
        case "My-room":
            item = _h.view(class_id, Room)
            if request.method == 'POST':
                if item.client_id == client_id:
                    item.client_id = None
                else:
                    item.client_id = client_id
                db.session.add(item)
                db.session.commit()
                return redirect(url_for("my_rooms"))
        case "Event":
            item = _h.view(class_id, Event)
        case "My-event":
            item = _h.view(class_id, Event)
        case "Service":
            item = _h.view(class_id, Service)
        case "My-service":
            item = _h.view(class_id, Service)
    return render_template('view-item.html', user=session['user'], logged=True, item=item, client_id=client_id)


@login_required
def logout_page():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for("login"))


@login_required
def remove_account_action():
    client = Client.query.filter_by(email=session['user']['email']).first()
    Item().delete(client.id, Client)
    return redirect(url_for('logout'))
