from flask import Blueprint, jsonify, request
from returns.result import Success, Failure

from repository.target_repository import get_all_targets, create_target, update_target, delete_target

target_blueprint = Blueprint('target', __name__)



@target_blueprint.route('/target', methods=['GET'])
def get_all_targets_c():
    result = get_all_targets()

    if isinstance(result, Success):
        targets = result.unwrap()
        return jsonify(targets), 200
    elif isinstance(result, Failure):
        error_message = result.failure()
        return jsonify({'error': error_message}), 500


@target_blueprint.route('/targets', methods=['POST'])
def create_target_c():
    target_data = request.json
    result = create_target(target_data)

    if isinstance(result, Success):
        return jsonify(result.unwrap()), 201
    elif isinstance(result, Failure):
        return jsonify({'error': result.failure()}), 400



@target_blueprint.route('/targets/<int:target_id>', methods=['PUT'])
def update_target_c(target_id):
    target_data = request.json
    result = update_target(target_id, target_data)

    if isinstance(result, Success):
        return jsonify(result.unwrap()), 200
    elif isinstance(result, Failure):
        return jsonify({'error': result.failure()}), 404



@target_blueprint.route('/targets/<int:target_id>', methods=['DELETE'])
def delete_target_c(target_id):
    result = delete_target(target_id)

    if isinstance(result, Success):
        return jsonify(result.unwrap()), 200
    elif isinstance(result, Failure):
        return jsonify({'error': result.failure()}), 404
