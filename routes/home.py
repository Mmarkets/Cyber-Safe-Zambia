from flask import Blueprint, render_template, session, request
from flask_login import current_user
from models import db, Usage
from datetime import datetime, timezone
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    logging.debug(f"Home request: user={current_user.email if current_user.is_authenticated else 'anonymous'}")
    if current_user.is_authenticated:
        try:
            usage = Usage(
                user_id=current_user.id,
                action='visit_home',
                timestamp=datetime.now(timezone.UTC)
            )
            db.session.add(usage)
            db.session.commit()
            logging.debug(f"Usage recorded for user {current_user.email}: action=visit_home")
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error recording usage: {e}")
    return render_template('home.html')