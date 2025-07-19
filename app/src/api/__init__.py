from flask_restful import Api, Resource, request, abort
from flask import session
from ..auth import hash_password
from ..models import User, Rooms
import logging

logging.basicConfig(level=logging.INFO)

def init_app(app):
    api = Api(app)

    class Register(Resource):
        def post(self):
            name = request.form.get('name').strip().capitalize()
            email = request.form.get('email').strip().lower()
            username = request.form.get('username').strip().lower()
            password = request.form.get('password').strip()
            confirm_password = request.form.get('confirm_password').strip()
            if password != confirm_password:
                return {"code": 400, "message": "As senhas não coincidem"}, 400
            if not User.exists(username=username):
                hash = hash_password(password)
                User.create(name=name, email=email, username=username, hash_password=hash)
                session["user_username"] = username
            else:
                return {"code": 409, "message": "Esse usuário já existe"}, 409
            
    api.add_resource(Register, '/api/register')
    
    class Login(Resource):
        def post(self):
            username = request.form.get('username').strip().lower()
            password = request.form.get('password').strip()
            user = User.get_by_username(username=username)
            if user and user.hash_password == hash_password(password):
                session["user_username"] = user.username
                return {"code": 200, "message": "Login bem-sucedido"}, 200
            else:
                return {"code": 401, "message": "Usuário ou senha inválidos"}, 401
            
    api.add_resource(Login, '/api/login')
    
    class RoomDetail(Resource):
        def get(self, room_id):
            room = Rooms.get_by_id(room_id)
            if not room:
                abort(404, "Quarto não encontrado")

            return {
                "id": room.id,
                "name": room.name,
                "description": room.description,
                "price": float(room.price),
                "image": room.image,
                "capacity": room.capacity
            }
            
    api.add_resource(RoomDetail, '/api/rooms/room/<int:room_id>')