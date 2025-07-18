from flask import render_template, request

def home_page():
    return render_template("home_page.html")

def rooms_page():
    return render_template("rooms.html")

def login_page(app):
    if request.method == 'POST':
        # Handle login logic here
        pass
    return render_template("login.html")

def contact_page():
    return render_template("contact.html")

def profile_page():
    return render_template("profile.html")

def my_rooms_page():
    return render_template("my_rooms.html")