from flask import render_template, request, session
from ..controller.actions import get_first_three_rooms
from ..models import User, Rooms, Services, Events, search_by_name, get_room_owner, UserEvent, UserService


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
            owner = room.user.username == username if room.user else False
            occupied = room.is_occupied(room.id)  # Verifica se o quarto está ocupado
            return render_template("selected_room.html", id=id, owner=owner, room=room, occupied=occupied)
        else:
            return render_template("404.html"), 404

    # Sem ID: mostra a listagem de quartos
    return render_template("rooms.html")



def services_page(id=None):
    username = session.get("user_username")
    if id:
        if not str(id).isdigit():
            return page_not_found_page(404)

        id = int(id)
        service = Services.get_by_id(id)

        if service:
            user = User.get_by_username(username=username)
            owner = UserService.find_by_user_and_service(user_id=user.id, service_id=id) is not None
            # owner = service.user.username == username if service.user else False
            return render_template("selected_service.html", id=id, owner=owner, service=service)
        else:
            return render_template("404.html"), 404
    return render_template("services.html")


def events_page(id=None):
    username = session.get("user_username")
    if id:
        if not str(id).isdigit():
            return page_not_found_page(404)

        id = int(id)
        event = Events.get_by_id(id)

        if event:
            user = User.get_by_username(username=username)
            owner = UserEvent.find_by_user_and_event(user_id=user.id, event_id=id) is not None
            # owner = event.user.username == username if event.user else False
            return render_template("selected_event.html", id=id, owner=owner, event=event)
        else:
            return render_template("404.html"), 404
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
