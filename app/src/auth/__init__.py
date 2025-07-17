from flask import render_template, session, redirect, url_for
from functools import wraps
import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_username' not in session:
            return redirect(url_for('auth'))
        return f(*args, **kwargs)

    return decorated_function


def init_app(app):
    @app.route("/auth", methods=["GET", "POST"])
    def auth():
        return render_template("login.html")
