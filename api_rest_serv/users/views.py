
from flask import Blueprint, jsonify
from api_rest_serv import logger, session, docs
from api_rest_serv.schemas import UserSchema, AuthSchema
from flask_apispec import use_kwargs, marshal_with
from api_rest_serv.models import User

users = Blueprint('users', __name__)


@users.route('/register', methods=['POST'])
@use_kwargs(UserSchema)
@marshal_with(AuthSchema)
def register(**kwargs):
    try:
        user = User(**kwargs)
        session.add(user)
        session.commit()
        token = user.get_token()
        logger.warning(f'user: {kwargs["email"]} - register user action success')
    except Exception as e:
        logger.warning(f'user: {kwargs["email"]} - register user action failed with errors: {e}')
        return {'message': str(e)}, 400
    return {'access_token': token}


@users.route('/login', methods=['POST'])
@use_kwargs(UserSchema(only=('email', 'password')))
@marshal_with(AuthSchema)
def login(**kwargs):
    try:
        user = User.authenticate(**kwargs)
        token = user.get_token()
        logger.warning(f'user: {user.email} - login user action success')
    except Exception as e:
        logger.warning(f'user: {kwargs["email"]} - login user action failed with errors: {e}')
        return {'message': str(e)}, 400
    return {'access_token': token}


@users.errorhandler(422)
def error_handler(err):
    headers = err.data.get('headers',None)
    messages = err.data.get('messages', ['Invalid customer request...'])
    logger.warning(f'Invalid input params: {messages}')
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400


docs.register(register, blueprint='users')
docs.register(login, blueprint='users')
