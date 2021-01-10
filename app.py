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
    'APISPEC_SWAGGER_URL':'/helper/'
})

from models import *

Base.metadata.create_all(bind=engine)


@app.route('/elements', methods=['GET'])
@jwt_required
@marshal_with(ElementSchema(many=True))
def get_list():
    user_n = get_jwt_identity()
    elements = NW_Elements.query.filter(NW_Elements.user_id==user_n)
    return elements


@app.route('/elements', methods=['POST'])
@jwt_required
@use_kwargs(ElementSchema)
@marshal_with(ElementSchema)
def update_list(**kwargs):
    user_n = get_jwt_identity()
    new_one = NW_Elements(user_id=user_n, **kwargs)
    session.add(new_one)
    session.commit()
    return new_one


@app.route('/elements/<int:element_id>', methods=['PUT'])
@jwt_required
@use_kwargs(ElementSchema)
@marshal_with(ElementSchema)
def update_element(element_id, **kwargs):
    user_n = get_jwt_identity()
    item = NW_Elements.query.filter(NW_Elements.id == element_id, NW_Elements.user_id==user_n).first()
    if not item:
        return {'message': 'No elements with this id'}, 400
    for key, value in kwargs.items():
        setattr(item, key, value)
    session.commit()
    return item

@app.route('/elements/<int:element_id>', methods=['DELETE'])
@jwt_required
@marshal_with(ElementSchema)
def delete_element(element_id):
    user_n = get_jwt_identity()
    item = NW_Elements.query.filter(NW_Elements.id == element_id, NW_Elements.user_id==user_n).first()
    if not item:
        return {'message': 'No tutorials with this id'}, 400
    session.delete(item)
    session.commit()
    return '', 204

@app.route('/register', methods=['POST'])
@use_kwargs(UserSchema)
@marshal_with(AuthSchema)
def register(**kwargs):
    user = User(**kwargs)
    session.add(user)
    session.commit()
    token = user.get_token()
    return {'access_token': token}


@app.route('/login', methods=['POST'])
@use_kwargs(UserSchema(only=('email', 'password')))
@marshal_with(AuthSchema)
def login(**kwargs):
    user = User.authenticate(**kwargs)
    token = user.get_token()
    return {'access_token': token}


@app.teardown_appcontext
def shutdown_session(exeption=None):
    session.remove()


docs.register(get_list)
docs.register(update_list)
docs.register(update_element)
docs.register(delete_element)
docs.register(register)
docs.register(login)


if __name__ == '__main__':
    app.run()

