from flask import Blueprint

# import functions from controller
from app.controllers.users_controller import (
    create_user,
    read_user,
    read_users,
    update_user,
    delete_user,
    login_user,
)

# set blueprint name and prefix
bp = Blueprint("bp_users", __name__, url_prefix="/users")

# declaring methods with associated endpoints and controller function
bp.post("/signup")(create_user)
bp.get("/profile")(read_user)
bp.get("")(read_users)
bp.patch("")(update_user)
bp.delete("")(delete_user)
bp.post("/signin")(login_user)
