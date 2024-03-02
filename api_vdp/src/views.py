from api_vdp.src.controller import (home_page, login_page, register_page, profile_page,
                                    logout_page, edit_profile_page, rooms_page, admin_page,
                                    events_page, catalog_item)


def init_app(app):
    @app.route("/")
    def home():
        return home_page()

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        return login_page(app)

    @app.route("/register", methods=['GET', 'POST'])
    def register():
        return register_page(app)

    @app.route("/profile", methods=['GET', 'POST'])
    def profile():
        return profile_page()

    @app.route("/edit-profile", methods=['GET', 'POST'])
    def edit_profile():
        return edit_profile_page()

    @app.route("/rooms", methods=['GET', 'POST'])
    def rooms():
        return rooms_page()

    @app.route("/events", methods=['GET', 'POST'])
    def events():
        return events_page()

    @app.route("/services", methods=['GET', 'POST'])
    def services():
        return home_page()

    @app.route("/rate-us", methods=['GET', 'POST'])
    def rate_us():
        return home_page()

    @app.route("/support", methods=['GET', 'POST'])
    def support():
        return home_page()

    @app.route("/logout")
    def logout():
        return logout_page()

    @app.route("/admin")
    def admin():
        return admin_page()

    @app.route("/checkin/<room_id>", methods=['GET', 'POST'])
    def checkin(room_id):
        return catalog_item(room_id)
