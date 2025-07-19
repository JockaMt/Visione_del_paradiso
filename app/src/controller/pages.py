from flask import render_template, request
from ..controller.actions import get_first_three_rooms
from ..models import Rooms, search_by_name


def home_page():
    return render_template("home_page.html", quartos=get_first_three_rooms())

def page_not_found_page(error):
    return render_template("404.html"), error.code

def rooms_page(id=None):
    if id:
        if Rooms.get_by_id(id):
            return render_template("selected_room.html", id=id)
        else:
            return render_template("404.html"), 404
    return render_template("rooms.html")


def services_page():
    return render_template("services.html")


def events_page():
    return render_template("events.html")


def contact_page():
    return render_template("contact.html")


def profile_page():
    return render_template("profile.html")


def my_rooms_page():
    return render_template("my_rooms.html")


def my_services_page():
    return render_template("my_services.html")


def my_events_page():
    return render_template("my_events.html")
