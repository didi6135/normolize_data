# from flask import Blueprint, jsonify
# from returns.result import Success, Failure
#
# from repository.mission_repository import get_all_missions
#
# mission_buleprint = Blueprint('users', __name__)
#
#
#
# @mission_buleprint.route('/mission', methods=['GET'])
# def get_all_missions_c():
#     missions_result = get_all_missions()
#
#     # Check if the result is Success or Failure
#     if isinstance(missions_result, Success):
#         # Unwrap the Success value and return it
#         missions = missions_result.unwrap()
#         return jsonify(missions), 200
#     elif isinstance(missions_result, Failure):
#         # Unwrap the Failure value and return an error response
#         error_message = missions_result.failure()
#         return jsonify({'error': error_message}), 500
#
#
# # @mission_buleprint.route('/mission/<mission_id:int>', methods=['GET'])
# # def get_mission_by_id(mission_id):
# #     pass