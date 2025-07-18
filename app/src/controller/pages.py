from flask import render_template, request
from ..controller.actions import get_first_three_rooms


def home_page():
    return render_template("home_page.html", quartos=get_first_three_rooms())


def rooms_page():
    return render_template("rooms.html")


def services_page():
    return render_template("services.html")


def events_page():
    return render_template("events.html")


def login_page():
    return render_template("login.html")


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
