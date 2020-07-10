# Develop vmgabriel

# Libraries
from flask import Flask, jsonify
from flask_jwt import JWT
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)

from config.server import configuration as conf

# Connection
from user.infraestructures.postgres.database_user import Database_User

# Routes
from protocols.http.v0.index import mod
from user.infraestructures.http.v0 import UserV0Http

persistency = conf['persistency']

user_service = Database_User(persistency)

list_routes = [
    UserV0Http(user_service)
]

app = Flask(__name__)

app.config['JWT_TOKEN_LOCATION'] = conf['jwt_location']
app.config['JWT_SECRET_KEY'] = conf['jwt_secret']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

jwt = JWTManager(app)

app.register_blueprint(mod, url_prefix='/api')
for route in list_routes:
    app.register_blueprint(route.get_blueprint(), url_prefix='/api/v0')

if __name__ == '__main__':
    app.run (
        host=conf['host'],
        debug=conf['debug'],
        port=conf['port']
    )


