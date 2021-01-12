

from typing import Optional, Dict
from flask import Flask, jsonify, request
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from config import Config
from apispec.ext.marshmallow import MarshmallowPlugin
from  apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from schemas import ElementSchema, UserSchema, AuthSchema
from flask_apispec import use_kwargs, marshal_with
import logging

app = Flask(__name__)
app.config.from_object(Config)

client = app.test_client()

engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

jwt = JWTManager(app)

docs = FlaskApiSpec()
docs.init_app(app)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='netelements',
        version='v1',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()]
    ),
    'APISPEC_SWAGGER_URL':'/swigger/'
})

from models import *

Base.metadata.create_all(bind=engine)

def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
    file_handler = logging.FileHandler('log/api.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


logger = setup_logger()


@app.route('/elements', methods=['GET'])
@jwt_required
@marshal_with(ElementSchema(many=True))
def get_list():
    try:
        user_n = get_jwt_identity()
  #      elements = NW_Elements.query.filter(NW_Elements.user_id==user_n).all()
        elements = NW_Elements.getElementList(user_id=user_n)
    except Exception as e:
        logger.warning(f'user:{user_n} elements - read action failed with errors: {e}')
        return {'message': str(e)}, 400
    return elements


@app.route('/elements', methods=['POST'])
@jwt_required
@use_kwargs(ElementSchema)
@marshal_with(ElementSchema)
def update_list(**kwargs):
    try:
        user_n = get_jwt_identity()
        new_one = NW_Elements(user_id=user_n, **kwargs)
        new_one.save()
    except Exception as e:
        logger.warning(f'user: {user_n}, elements - create action failed with errors: {e}')
        return {'message': str(e)}, 400
    return new_one


@app.route('/elements/<int:element_id>', methods=['PUT'])
@jwt_required
@use_kwargs(ElementSchema)
@marshal_with(ElementSchema)
def update_element(element_id, **kwargs):
    try:
        user_n = get_jwt_identity()
        item = NW_Elements.get(element_id, user_n)
        item.update(**kwargs)
    except Exception as e:
        logger.warning(f'user: {user_n}, element id: {element_id} - update action failed with errors: {e}')
        return {'message': str(e)}, 400
    return item


@app.route('/elements/<int:element_id>', methods=['DELETE'])
@jwt_required
@marshal_with(ElementSchema)
def delete_element(element_id):
    try:
        user_n = get_jwt_identity()
        item = NW_Elements.get(element_id, user_n)
        item.delete()
    except Exception as e:
        logger.warning(f'user: {user_n}, element id: {element_id} - delete action failed with errors: {e}')
        return {'message': str(e)}, 400
    return '', 204


@app.route('/register', methods=['POST'])
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


@app.route('/login', methods=['POST'])
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


@app.teardown_appcontext
def shutdown_session(exeption=None):
    session.remove()
    logger.warning(f'Close servers')

@app.errorhandler(422)
def error_handler(err):
    headers = err.data.get('headers',None)
    messages = err.data.get('messages', ['Invalid customer request...'])
    logger.warning(f'Invalid input params: {massages}')
    if headers:
        return jsonify({'message': messages }), 400, headers
    else:
        return jsonify({'message': messages}), 400


docs.register(get_list)
docs.register(update_list)
docs.register(update_element)
docs.register(delete_element)
docs.register(register)
docs.register(login)


if __name__ == '__main__':
    logger.warning(f'Start server')
    app.run()

