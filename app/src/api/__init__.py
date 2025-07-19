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
                session["user_name"] = name
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
                session["user_name"] = user.name
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
                "capacity": room.capacity,
                "occupied": room.user_id is not None
            }
            
    api.add_resource(RoomDetail, '/api/rooms/room/<int:room_id>')
    
    class ReserveRoom(Resource):
        def post(self, room_id):
            username = session.get("user_username")
            if not username:
                abort(401, message="Usuário não autenticado")

            room = Rooms.get_by_id(room_id)
            if not room:
                abort(404, message="Quarto não encontrado")

            if room.user_id is not None:
                abort(400, message="Quarto já reservado")

            user = User.get_by_username(username=username)
            Rooms.update(room_id, user_id=user.id)
            return {"message": "Quarto reservado com sucesso"}, 200
        
    api.add_resource(ReserveRoom, '/api/rooms/reserve/<int:room_id>')
    
    class CancelReservation(Resource):
        def post(self, room_id):
            username = session.get("user_username")
            if not username:
                abort(401, message="Usuário não autenticado")

            room = Rooms.get_by_id(room_id)
            if not room:
                abort(404, message="Quarto não encontrado")

            if room.user_id is None or room.user.username != username:
                abort(400, message="Quarto não reservado por este usuário")

            Rooms.update(room_id, user_id=None)
            return {"message": "Reserva cancelada com sucesso"}, 200
        
    api.add_resource(CancelReservation, '/api/rooms/cancel/<int:room_id>')
    
    class GetUserDetail(Resource):
        def get(self):
            username = session.get("user_username")
            if not username:
                abort(401, message="Usuário não autenticado")

            user = User.get_by_username(username=username)
            if not user:
                abort(404, message="Usuário não encontrado")

            return {
                "username": user.username,
                "name": user.name,
                "email": user.email,
                "avatar": user.avatar,
                "rooms_count": len(user.rooms),
                "services_count": len(user.services),
                "events_count": len(user.events)
            }, 200  # status code explícito
            
    api.add_resource(GetUserDetail, '/api/user/details')
    
    class GetUserProfile(Resource):
        def get(self):
            username = session.get("user_username")
            if not username:
                abort(401, message="Usuário não autenticado")

            user = User.get_by_username(username=username)
            if not user:
                abort(404, message="Usuário não encontrado")

            return {
                "username": user.username,
                "name": user.name,
                "email": user.email,
                "avatar": user.avatar
            }, 200
            
    api.add_resource(GetUserProfile, '/api/user/profile')
    
    class EditProfile(Resource):
        def post(self):
            username = session.get("user_username")
            if not username:
                abort(401, message="Usuário não autenticado")

            user = User.get_by_username(username=username)
            print(user)
            if not user:
                abort(404, message="Usuário não encontrado")

            name = request.form.get('name')
            email = request.form.get('email')
            avatar = request.form.get('avatar')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')

            update_fields = {}

            if name is not None and name.strip():
                update_fields['name'] = name.strip().capitalize()
            if email is not None and email.strip():
                update_fields['email'] = email.strip().lower()
            if avatar is not None and avatar.strip():
                update_fields['avatar'] = avatar.strip()

            if password is not None and password.strip():
                if password != confirm_password:
                    return {"code": 400, "message": "As senhas não coincidem"}, 400
                update_fields['hash_password'] = hash_password(password.strip())

            if update_fields:
                User.update(user.username, **update_fields)
                session["user_username"] = update_fields.get('username', user.username)
                session["user_name"] = update_fields.get('name', user.name)
                return {"message": "Perfil atualizado com sucesso", "code": 200}, 200
            else:
                return {"message": "Nenhuma alteração realizada"}, 200
            
    api.add_resource(EditProfile, '/api/user/edit')