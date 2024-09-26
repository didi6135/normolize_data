from flask import Blueprint

mission_buleprint = Blueprint('users', __name__)



@mission_buleprint.route('/missions', methods=['GET'])
def get_all_missions:
    pass