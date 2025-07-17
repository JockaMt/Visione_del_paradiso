from flask import redirect, url_for, request, render_template


def logout_action():
    return redirect(url_for('auth'))


def register_action():
    name = request.form.get('name').strip().capitalize()
    email = request.form.get('email').strip().lower()
    username = request.form.get('username').strip().lower()
    return redirect(url_for('home'))