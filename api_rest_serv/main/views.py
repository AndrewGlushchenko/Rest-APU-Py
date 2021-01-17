
from flask import Blueprint, jsonify
from api_rest_serv import logger, docs
from api_rest_serv.schemas import ElementSchema
from flask_apispec import use_kwargs, marshal_with
from api_rest_serv.models import NW_Elements
from flask_jwt_extended import jwt_required, get_jwt_identity

elements = Blueprint('elements', __name__)


@elements.route('/elements', methods=['GET'])
@jwt_required
@marshal_with(ElementSchema(many=True))
def get_list():
    try:
        user_n = get_jwt_identity()
        n_elements = NW_Elements.getElementList(user_id=user_n)
    except Exception as e:
        logger.warning(f'user:{user_n} elements - read action failed with errors: {e}')
        return {'message': str(e)}, 400
    return n_elements


@elements.route('/elements', methods=['POST'])
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


@elements.route('/elements/<int:element_id>', methods=['PUT'])
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


@elements.route('/elements/<int:element_id>', methods=['DELETE'])
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


@elements.errorhandler(422)
def error_handler(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid customer request...'])
    logger.warning(f'Invalid input params: {messages}')
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400


docs.register(get_list, blueprint='elements')
docs.register(update_list, blueprint='elements')
docs.register(update_element, blueprint='elements')
docs.register(delete_element, blueprint='elements')