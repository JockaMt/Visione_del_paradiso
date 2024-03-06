from functools import wraps
from flask import redirect, url_for, session


def cripto(password, secret):
    cod = ""
    for i in password:
        cod = cod + chr((ord(i) + secret) % 127)
    return cod


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
