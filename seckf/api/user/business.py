import random
from datetime import datetime, timedelta

import jwt
from flask import abort
from flask_bcrypt import generate_password_hash, check_password_hash

from seckf import settings
from seckf.api.security import log, val_num
from seckf.database import db
from seckf.database.privileges import Privilege
from seckf.database.users import User


def activate_user(user_id, data):
    username = strip_whitespace_from_username(data.get("username"))
    result = get_user_result_by_id(user_id)
    user_is_already_activated(result.activated)
    compare_email(result.email, data.get('email'))
    compare_passwords(data.get('password'), data.get('repassword'))
    compare_access_tokens(result.accessToken, data.get('accessToken'))
    pw_hash = generate_password_hash(data.get('password')).decode('utf-8')
    activate_account(username, pw_hash, user_id)
    log("User is activated", "HIGH", "PASS")
    return {'message': 'User successfully activated'}


def login_user(data):
    user = get_user_result_by_username(data.get("username"))
    is_user_activated(user)
    does_user_has_access(user)
    check_password(user, data.get("password"))
    log("User successfully logedin", "HIGH", "PASS")
    token = create_jwt_token_for_user(user)
    return {'Authorization token': token, 'username': user.username}


def login_skip():
    log("Anonymous user successfully logedin", "HIGH", "PASS")
    token = create_jwt_token_for_user("anonymous")
    return {'Authorization token': token, 'username': "anonymous"}


def create_user(data):
    log("A new user created", "MEDIUM", "PASS")
    my_secure_rng = random.SystemRandom()
    try:
        user = User(data.get('email'))
        user.privilege_id = data.get('privilege_id')
        user.username = data.get('username')
        user.accessToken = my_secure_rng.randrange(10000000, 99999999)
        user.group_id = 0
        db.session.add(user)
        db.session.commit()
    except:
        db.session.rollback()
        return abort(400, 'User could not be created')
    result = User.query.filter(User.email == data.get('email')).one()
    return result


def manage_user(user_id, data):
    log("Manage user triggered", "HIGH", "PASS")
    user = get_user_result_by_id(user_id)
    if data.get('active'):
        user.access = data.get('active').lower() == 'true'
    if data.get('privilege_id'):
        user.privilege_id = data.get('privilege_id')
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        log("User triggered error managing failed: {}".format(e), "HIGH", "FAIL")
        return {'message': 'User could not be managed'}
    return {'message': 'User successfully managed'}


def list_users():
    log("Overview of list users triggered", "HIGH", "PASS")
    result = User.query.paginate(1, 2500, False)
    return result


def get_user_result_by_username(username):
    try:
        user = User.query.filter(User.username == username).one()
        return user
    except:
        return abort(400, 'Login was failed')


def is_user_activated(user):
    if not user.activated:
        return abort(400, 'Login was failed')


def does_user_has_access(user):
    if not user.access:
        return abort(400, 'Login was failed')


def check_password(password_from_db, supplied_password):
    if not check_password_hash(password_from_db.password, supplied_password):
        return abort(400, 'Login was failed')


def create_jwt_token_for_user(user):
    if user == 'anonymous':
        payload = {
            'UserId': random.randint(99999, 999999),
            'iat': datetime.utcnow(),
            'privilege': "edit:read",
            'exp': datetime.utcnow() + timedelta(minutes=120)
        }
    else:
        payload = {
            'UserId': user.id,
            'iat': datetime.utcnow(),
            'privilege': user.privilege.privilege,
            'exp': datetime.utcnow() + timedelta(minutes=120)
        }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')
    return token


def get_user_result_by_id(user_id):
    return User.query.filter(User.id == user_id).one()


def strip_whitespace_from_username(username):
    refactor = username.replace(" ", "")
    return refactor


def user_is_already_activated(result):
    if result == True:
        return abort(400, 'User could not be activated')


def compare_email(email_from_query, email_from_form):
    if email_from_query != email_from_form:
        return abort(400, 'User could not be activated')


def compare_passwords(password, repassword):
    if password != repassword:
        return abort(400, 'User could not be activated')


def compare_access_tokens(token_from_query, token_from_form):
    val_num(token_from_form)
    if token_from_query != token_from_form:
        return abort(400, 'User could not be activated')


def activate_account(username, pw_hash, user_id):
    activate = get_user_result_by_id(user_id)
    activate.password = pw_hash
    activate.access = True
    activate.activated = True
    activate.username = username
    db.session.add(activate)
    db.session.commit()


def list_privileges():
    log("User requested privileges items", "MEDIUM", "PASS")
    result = Privilege.query.paginate(1, 2500, False)
    return result
