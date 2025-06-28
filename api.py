from flask_restful import Api, Resource, reqparse
from flask import Blueprint, request, jsonify
from controllers.phishing_controller import check_phishing
from config import Config
import logging
from flask_login import login_required
from datetime import datetime

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

parser = reqparse.RequestParser()
parser.add_argument('url', type=str, required=True, help="URL is required")
parser.add_argument('api_key', type=str, required=True, location='headers', help="API key is required in headers")

class PhishingCheck(Resource):
    def post(self):
        try:
            data = request.get_json()
            api_key = request.headers.get('api_key')
            logging.info(f"Raw headers: {request.headers}")
            logging.info(f"API request with api_key: {api_key}, url: {data.get('url')}")
            if not api_key or api_key != Config.API_KEY:
                logging.warning(f"Invalid or missing API key: {api_key}")
                return {'error': 'Invalid or missing API key'}, 401
            if not data or 'url' not in data:
                return {'error': 'URL is required'}, 400
            result = check_phishing(data['url'])
            return result, 200
        except Exception as e:
            logging.error(f"API error: {str(e)}")
            return {'error': str(e)}, 500

api.add_resource(PhishingCheck, '/api/phishing')

@api_bp.route('/api/threats')
@login_required
def get_threats():
    # Mock data
    threats = [
        {'id': 1, 'type': 'Phishing', 'severity': 'High', 'timestamp': '2025-06-19 09:00', 'ip_address': '192.168.1.1', 'actions': ''},
        {'id': 2, 'type': 'Malware', 'severity': 'Medium', 'timestamp': '2025-06-18 15:30', 'ip_address': '10.0.0.2', 'actions': ''}
    ]
    return jsonify({'data': threats})

@api_bp.route('/api/user_behavior')
@login_required
def get_user_behavior():
    users = User.query.all()
    user_data = [
        {
            'user_id': user.id,
            'username': user.username,
            'failed_logins': 0,  # Placeholder; implement actual logic
            'last_activity': user.last_activity.isoformat() if user.last_activity else 'Never',
            'status': 'Normal' if user.last_activity else 'Inactive'
        } for user in users
    ]
    return jsonify({'data': user_data})