from app.configs.database import db
from app.models.users_model import UsersModel
from flask import jsonify, request
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

def create_user():
    #starting db session
    #retrieving data from the request
    session: Session = db.session
    data = request.get_json()

    #checking request keys vs expected keys and, in case of error, return to the user what's needed
    expected_keys = ["user_name", "email", "password"]
    entry_keys = [k for k in data.keys()]
    try:
        for key in entry_keys:
            if key not in expected_keys:
                raise KeyError
    except:
        wrong_keys = []
        for key in entry_keys:
            if key not in expected_keys:
                wrong_keys.append(key)
        return {
            "error": "unexpected keys",
            "expected_keys": expected_keys,
            "wrong_keys": wrong_keys,
        }, 400

    #normalizing request data according to db rules
    data["user_name"] = data["user_name"].title()
    data["email"] = data["email"].lower()

    #creating model from request data
    new_user = UsersModel(**data)

    # add user, commit changes in case of error tell the user what's wrong
    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError as e:
        if type(e.orig) == UniqueViolation:
            return {"error": "username or email already used"}, 409

    #returning the created object and created status
    return jsonify(new_user), 201


#this decorator means the route requires a json web token in the request
@jwt_required()
def read_users():
    #starting db session
    session: Session = db.session

    #get all users from db in a list
    users_list = session.query(UsersModel).all()

    #return an error message if there's no data
    if len(users_list) == 0:
        return {"error": "no users on database"}, 404

    #return list of users and ok status
    return jsonify(users_list), 200


@jwt_required()
def read_user():
    #starting db session
    session: Session = db.session

    #identify the user from the token given in the request
    #search for the user in the db using the primary key "id"
    user = get_jwt_identity()
    selected_user = UsersModel.query.get(user["id"])

    #check if user exists and return an error message/404 if it doesn't
    if not selected_user:
        return {"error": "user not found"}, 404

    #return user info and ok status
    return jsonify(selected_user), 200


@jwt_required()
def update_user():
    #starting db session
    #retrieving data from the request
    session: Session = db.session
    data = request.get_json()

    #specify what can be updated and check request for keys
    #checking request keys vs updatable keys and, in case of error, return to the user what's wrong
    updatable_data = ["email", "password"]
    entry_keys = [k for k in data.keys()]
    try:
        for key in entry_keys:
            if key not in updatable_data:
                raise KeyError
    except:
        wrong_keys = []
        for key in entry_keys:
            if key not in updatable_data:
                wrong_keys.append(key)
        return {
            "error": "not updatable",
            "updatable_data": updatable_data,
            "wrong_keys": wrong_keys,
        }, 400

    #normalize data
    data["email"] = data["email"].lower()

    #register update time
    now = datetime.utcnow()
    data["update_date"] = now

    #identify the user from the token given in the request
    #search for the user in the db using the primary key "id"
    user = get_jwt_identity()
    selected_user = UsersModel.query.get(user["id"])

    #check user existence
    if not selected_user:
        return {"error": "user not found"}, 404

    #updating data with data from the request
    for key, value in data.items():
        setattr(selected_user, key, value)

    # add and commit changes, in case of error tell the user what's wrong
    try:
        session.add(selected_user)
        session.commit()
    except IntegrityError as e:
        if type(e.orig == UniqueViolation):
            return {"error": "email already exists"}, 409

    #return updated user
    return jsonify(selected_user), 200


@jwt_required()
def delete_user():
    #starting db session
    session: Session = db.session

    #identify the user from the token given in the request
    #search for the user in the db using the primary key "id"
    user = get_jwt_identity()
    selected_user = UsersModel.query.get(user["id"])

    #check user existence, delete user, commit changes and return no content
    if selected_user:
        session.delete(selected_user)
        session.commit()

        return "", 204

    #if no selected_user, return 404
    return {"error": "user not found"}, 404


def login_user():
    #retrieving data from request
    data = request.get_json()

    #search for user by email sent in request
    user: UsersModel = UsersModel.query.filter_by(email=data["email"]).first()

    #check user existence
    if not user:
        return {"error": "email not registered"}, 404

    #password check (using flask_jwt_extended library) with password from the request
    if not user.check_password(data["password"]):
        return {"error": "wrong email/password"}, 401

    #creating a token (using flask_jwt_extended library) with the user found and timelimit
    token = create_access_token(user, expires_delta=timedelta(minutes=30))

    #returning the access token and ok status
    return {"token": token}, 200
