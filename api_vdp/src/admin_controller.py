from datetime import datetime
from api_vdp.src.database import db
from api_vdp.src.model import Client, Room, Event, Service
from flask import session, render_template, redirect, url_for, request
from api_vdp.src.auth import login_required


@login_required
def admin_page():
    user = Client.query.filter_by(admin=session['user']['admin'].first()
    if user.admin:
        return render_template('admin.html', user=session['user'], logged=True)
    return redirect(url_for('home'))


def init_app(app):
    @app.route('/create_room', methods=['POST'])
    def create_room():
        if request.method == 'POST':
            name = request.form.get('room_name')
            description = request.form.get('room_description')
            size = request.form.get('room_size')
            price = request.form.get('room_price')
            room = Room(name=name, description=description, size=size, price=price)
            db.session.add(room)
            db.session.commit()
            return redirect(url_for('admin'))
        return render_template('admin.html')

    @app.route('/create_service', methods=['POST'])
    def create_service():
        if request.method == 'POST':
            name = request.form.get('service_name')
            description = request.form.get('service_description')
            size = request.form.get('service_size')
            service = Service(name=name, description=description, size=size, date=datetime.now())
            db.session.add(service)
            db.session.commit()
            return redirect(url_for('admin'))
        return render_template('admin.html')

    @app.route('/create_event', methods=['POST'])
    def create_event():
        if request.method == 'POST':
            name = request.form.get('event_name')
            description = request.form.get('event_description')
            size = request.form.get('event_size')
            event = Event(name=name, description=description, size=size, date=datetime.now())
            db.session.add(event)
            db.session.commit()
            return redirect(url_for('admin'))
        return render_template('admin.html')
