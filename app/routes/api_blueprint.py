from flask import Blueprint

#import blueprints
from app.routes.users_blueprint import bp as bp_users

#set blueprint name and prefix            
bp_api = Blueprint("bp_api", __name__, url_prefix="/api")

#register blueprints
bp_api.register_blueprint(bp_users)