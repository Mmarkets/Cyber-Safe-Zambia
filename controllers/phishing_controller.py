import requests
import bleach
from config import Config
import logging
from controllers.analytics_controller import log_usage
from flask_login import current_user
from models import db, ScanHistory

def check_phishing(url):
    log_usage('phishing')
    if not url or not url.startswith(('http://', 'https://')):
        return {'status': 'Invalid URL', 'category': 'danger'}
    try:
        clean_url = bleach.clean(url)
        api_key = Config.GOOGLE_SAFE_BROWSING_API_KEY
        endpoint = 'https://safebrowsing.googleapis.com/v4/threatMatches:find'
        payload = {
            'client': {'clientId': 'CyberSafeZambia', 'clientVersion': '1.0'},
            'threatInfo': {
                'threatTypes': ['MALWARE', 'SOCIAL_ENGINEERING', 'UNWANTED_SOFTWARE'],
                'platformTypes': ['ANY_PLATFORM'],
                'threatEntryTypes': ['URL'],
                'threatEntries': [{'url': clean_url}]
            }
        }
        response = requests.post(endpoint, params={'key': api_key}, json=payload)
        response.raise_for_status()
        data = response.json()
        result = {
            'status': 'Phishing or Malware Detected' if 'matches' in data else 'Safe',
            'category': 'danger' if 'matches' in data else 'success'
        }
        # Log scan history for authenticated users
        if current_user.is_authenticated:
            scan = ScanHistory(
                user_id=current_user.id,
                tool_name='phishing',
                input_data=clean_url[:255],
                result=result['status']
            )
            db.session.add(scan)
            db.session.commit()
            logging.info(f"Scan saved for user {current_user.id}: {clean_url}")
        return result
    except Exception as e:
        logging.error(f"Phishing check error: {str(e)}")
        return {'status': f'Error: {str(e)}', 'category': 'danger'}
