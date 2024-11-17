from flask import request, jsonify
from controllers.investor_login import investor_login
from controllers.startup_login import startup_login
from controllers.startup_details import equity_structure
from controllers.recommend_startups import recommend_startups

def init_routes(app):
    # Mapping the /login route to the login function
    app.route('/investor-login', methods=['POST'])(investor_login)
    app.route('/startup-login', methods=['POST'])(startup_login)
    app.route('/equity-structure', methods=['POST'])(equity_structure)
    app.route('/recommend-startups', methods=['POST'])(recommend_startups)