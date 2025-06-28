from flask import Blueprint, jsonify
from flask_login import login_required

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/v1/status', methods=['GET'])
@login_required
def status():
    return jsonify({'status': 'API is online'})