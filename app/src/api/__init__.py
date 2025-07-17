from flask_restful import Api, Resource, request
from flask import session
from ..auth import hash_password
from ..models import User
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
            else:
                return {"code": 409, "message": "Esse usuário já existe"}, 409
            
    api.add_resource(Register, '/register')
    
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
            
    api.add_resource(Login, '/login')