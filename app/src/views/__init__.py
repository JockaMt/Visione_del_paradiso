from ..controller.pages import (
    home_page,
    rooms_page,
    contact_page,
    profile_page,
    my_rooms_page,
    my_services_page,
    my_events_page,
    services_page,
    events_page,
)
from ..controller.actions import logout_action, buscar_action
from ..auth import login_required


def init_app(app):
    @app.route("/")
    def home():
        return home_page()

    @app.route("/rooms")
    def rooms():
        return rooms_page()

    @app.route("/services")
    def services():
        return services_page()

    @app.route("/events")
    def events():
        return events_page()

    @app.route("/logout")
    def logout():
        return logout_action()

    @app.route("/contact")
    def contact():
        # Implement contact page logic here
        return contact_page()

    @app.route("/profile", methods=["GET", "POST"])
    @login_required
    def profile():
        # Implement profile page logic here
        return profile_page()

    @app.route("/buscar")
    def buscar():
        return buscar_action()

    @app.route("/my-rooms", methods=["GET", "POST"])
    @login_required
    def my_rooms():
        return my_rooms_page()

    @app.route("/my-events", methods=["GET", "POST"])
    @login_required
    def my_events():
        return my_events_page()

    @app.route("/my-services", methods=["GET", "POST"])
    @login_required
    def my_services():
        return my_services_page()

    # @app.route("/register", methods=['GET', 'POST'])
    # def register():
    #     return register_page(app)

    # @app.route("/profile", methods=['GET', 'POST'])
    # def profile():
    #     return profile_page()

    # @app.route("/edit-profile", methods=['GET', 'POST'])
    # def edit_profile():
    #     return edit_profile_page()

    # @app.route("/rooms", methods=['GET', 'POST'])
    # def rooms():
    #     return rooms_page()

    # @app.route("/my-events", methods=['GET', 'POST'])
    # def my_events():
    #     return my_events_page()

    # @app.route("/my-services", methods=['GET', 'POST'])
    # def my_services():
    #     return my_services_page()

    # @app.route("/events", methods=['GET', 'POST'])
    # def events():
    #     return events_page()

    # @app.route("/services", methods=['GET', 'POST'])
    # def services():
    #     return services_page()

    # @app.route("/support", methods=['GET', 'POST'])
    # def support():
    #     return support_page()

    # @app.route("/logout")
    # def logout():
    #     return logout_page()

    # @app.route("/remove_account", methods=['GET'])
    # def remove_account():
    #     return remove_account_action()

    # @app.route("/admin")
    # def admin():
    #     return admin_page()

    # @app.route("/checkout/<item_name>-<item_id>", methods=['GET', 'POST'])
    # def checkin(item_id, item_name):
    #     return catalog_item(item_id, item_name.capitalize())
