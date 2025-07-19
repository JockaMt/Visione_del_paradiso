from flask import render_template, request, session
from ..controller.actions import get_first_three_rooms
from ..models import Rooms, search_by_name, get_room_owner


def home_page():
    return render_template("home_page.html", quartos=get_first_three_rooms())

def page_not_found_page(error):
    return render_template("404.html"), error.code

def rooms_page(id=None):
    username = session.get("user_username")

    # Validação do ID
    if id:
        if not str(id).isdigit():
            return page_not_found_page(404)

        id = int(id)
        room = Rooms.get_by_id(id)

        if room:
            room_owner = get_room_owner(id)
            owner = room_owner == username
            return render_template("selected_room.html", id=id, owner=owner)
        else:
            return render_template("404.html"), 404

    # Sem ID: mostra a listagem de quartos
    return render_template("rooms.html")



def services_page():
    return render_template("services.html")


def events_page():
    return render_template("events.html")


def contact_page():
    return render_template("contact.html")


def profile_page():
    return render_template("profile.html")

def edit_profile_page():
    return render_template("edit_profile.html")

def my_rooms_page():
    current_username = session.get("user_username")
    return render_template("my_rooms.html", username=current_username)


def my_services_page():
    current_username = session.get("user_username")
    return render_template("my_services.html", username=current_username)


def my_events_page():
    current_username = session.get("user_username")
    return render_template("my_events.html", username=current_username)
