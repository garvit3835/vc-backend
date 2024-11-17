from flask import request, jsonify
from controllers.investor_login import investor_login
from controllers.startup_login import startup_login

def init_routes(app):
    # Mapping the /login route to the login function
    app.route('/investor-login', methods=['POST'])(investor_login)
    app.route('/startup-login', methods=['POST'])(startup_login)
    app.route('/startup-login', methods=['POST'])(startup_login)