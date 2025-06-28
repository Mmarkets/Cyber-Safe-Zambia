from flask import current_app
from models import db, Usage
import logging
from datetime import datetime

def log_usage(tool_name):
    try:
        usage = Usage(tool_name=tool_name)
        db.session.add(usage)
        db.session.commit()
        logging.info(f"Tool used: {tool_name}")
    except Exception as e:
        logging.error(f"Analytics error: {str(e)}")

def get_usage_stats():
    try:
        stats = {
            'phishing': Usage.query.filter_by(tool_name='phishing').count(),
            'password_strength': Usage.query.filter_by(tool_name='password_strength').count(),
            'password_generator': Usage.query.filter_by(tool_name='password_generator').count(),
            'breach_checker': Usage.query.filter_by(tool_name='breach_checker').count(),
            'malware_scanner': Usage.query.filter_by(tool_name='malware_scanner').count()
        }
        return stats
    except Exception as e:
        logging.error(f"Stats retrieval error: {str(e)}")
        return {}