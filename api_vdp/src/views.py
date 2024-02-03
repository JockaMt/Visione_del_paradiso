from api_vdp.src.controller import home_page, login_page, register_page, profile_page, logout_page

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
    
    @app.route("/logout")
    def logout():
        return logout_page()