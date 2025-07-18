from flask import redirect, url_for, session, jsonify, request
from ..models import User, Rooms, search_by_name
import json


def logout_action():
    session.pop("user_username", None)
    return redirect(url_for('auth'))

def get_users():
    users = User.list_all()
    dictionary_users = [user.__dict__ for user in users]
    json_users = json.dumps(dictionary_users, default=str)
    return json_users

def buscar_action():
    termo = request.args.get('termo', '').strip().lower()

    # Busca filtrada no banco
    rooms = search_by_name(Rooms, termo)

    # Converte os objetos para dicionário (JSON serializável)
    resultados = [
        {
            "title": room.name,
            "description": room.description or "Sem descrição",
            "price": f"R$ {room.price:.2f}",
            "image": "https://images.pexels.com/photos/19836801/pexels-photo-19836801.jpeg"
        }
        for room in rooms
    ]

    return jsonify(resultados)