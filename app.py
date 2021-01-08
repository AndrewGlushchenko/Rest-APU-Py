from typing import Optional, Dict

from flask import Flask, jsonify, request
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

client = app.test_client()

engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

jwt = JWTManager(app)

from models import *

Base.metadata.create_all(bind=engine)


@app.route('/elements', methods=['GET'])
def get_list():
    elements = NW_Elements.query.all()
    serialized = []
    for element in elements:
        serialized.append({
            'id':element.id,
            'ip_address': element.ip_address,
            'name': element.name,
            'description': element.description
        })
    return jsonify(serialized)


@app.route('/elements', methods=['POST'])
def update_list():
    new_one = NW_Elements(**request.json)
    session.add(new_one)
    session.commit()
    serialized = {
        'id': new_one.id,
        'ip_address': new_one.ip_address,
        'name': new_one.name,
        'description': new_one.description
    }
    return jsonify(serialized)


@app.route('/elements/<int:element_id>', methods=['PUT'])
def update_element(element_id):
    item = NW_Elements.query.filter(NW_Elements.id == element_id).first()
    params = request.json
    if not item:
        return {'message': 'No elements with this id'}, 400
    for key, value in params.items():
        setattr(item, key, value)
    session.commit()
    serialized = {
        'id': item.id,
        'ip_address': item.ip_address,
        'name': item.name,
        'description': item.description
    }
    return serialized

@app.route('/elements/<int:element_id>', methods=['DELETE'])
def delete_element(element_id):
    item = NW_Elements.query.filter(NW_Elements.id == element_id).first()
    if not item:
        return {'message': 'No tutorials with this id'}, 400
    session.delete(item)
    session.commit()
    return '', 204

@app.route('/register', methods=['POST'])
def register():
    params = request.json
    user = User(**params)
    session.add(user)
    session.commit()
    token = user.get_token()
    return {'access_token': token}


@app.teardown_appcontext
def shutdown_session(exeption=None):
    session.remove()


if __name__ == '__main__':
    app.run()

