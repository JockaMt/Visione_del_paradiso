from flask import redirect, url_for, session, jsonify, request
from ..models import User, Rooms, Services, Events, search_by_name, search_by_name_with_user, search_service_by_name_with_user_from_relation, search_event_by_name_with_user_from_relation
import json


def logout_action():
    session.pop("user_username", None)
    session.pop("user_name", None)
    return redirect(url_for('auth'))

def get_users():
    users = User.list_all()
    dictionary_users = [user.__dict__ for user in users]
    json_users = json.dumps(dictionary_users, default=str)
    return json_users

def get_first_three_rooms():
    rooms = Rooms.list_all()[:3]
    return rooms

def serialize_result(obj):
    return {
        "id": getattr(obj, 'id', None),
        "title": getattr(obj, 'name', 'Sem título'),
        "description": getattr(obj, 'description', 'Sem descrição'),
        "price": f"R$ {getattr(obj, 'price', 0):.2f}" if hasattr(obj, 'price') else None,
        "image": getattr(obj, 'image', "https://images.pexels.com/photos/19836801/pexels-photo-19836801.jpeg"),
        "capacity": getattr(obj, 'capacity', None),
    }

def buscar_action():
    termo = request.args.get('termo', '').strip().lower()
    searchType = request.args.get('type', '').strip().lower()
    username = request.args.get('user', '').strip().lower()
    searchItem = None
    
    # Busca filtrada no banco
    if (searchType == 'rooms'):
        if username:
            searchItem = search_by_name_with_user(Rooms, termo, username)
        else:
            searchItem = search_by_name(Rooms, termo)
    elif (searchType == 'services'):
        if username:
            searchItem = search_service_by_name_with_user_from_relation(termo, username)
        else:
            searchItem = search_by_name(Services, termo)
    elif (searchType == 'events'):
        if username:
            searchItem = search_event_by_name_with_user_from_relation(termo, username)
        else:
            searchItem = search_by_name(Events, termo)

    # Converte os objetos para dicionário (JSON serializável)
    resultados = [serialize_result(i) for i in searchItem]

    if not searchItem:
        return jsonify([]) 
    
    return jsonify(resultados)