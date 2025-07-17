from flask import redirect, url_for, session
from ..models import User
import json


def logout_action():
    session.pop("user_username", None)
    return redirect(url_for('auth'))

def get_users():
    users = User.list_all()
    dictionary_users = [user.__dict__ for user in users]
    json_users = json.dumps(dictionary_users, default=str)
    return json_users