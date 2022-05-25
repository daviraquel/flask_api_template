from flask import Flask
from app.configs import migrations, database, env_configs, jwt_auth
from app import routes

def create_app() -> Flask:
    app = Flask(__name__)

    env_configs.init_app(app)
    database.init_app(app)
    migrations.init_app(app)
    jwt_auth.init_app(app)
    routes.init_app(app)

    return app
