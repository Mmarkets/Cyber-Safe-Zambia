from flask import Flask, session, jsonify, request
from flask_login import LoginManager, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_socketio import SocketIO
from flask_mail import Mail
from models import db, User, Threat, Usage, OTP, AuditLog, Scan
import os
import logging
from datetime import datetime
from threading import Thread
import time
import requests

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secure_random_key')  # Replace with unique key
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "app.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'Africa/Lusaka'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = './translations'
app.config['CACHE_TYPE'] = 'simple'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

db.init_app(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
babel = Babel(app)
cache = Cache(app)
mail = Mail(app)
socketio = SocketIO(app, async_mode='eventlet')
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour"],
    storage_uri="memory://"
)

@babel.localeselector
def get_locale():
    locale = request.args.get('lang', session.get('lang', app.config['BABEL_DEFAULT_LOCALE']))
    logging.debug(f"Selected locale: {locale}")
    return locale

   # Make get_locale available to Jinja2 templates
app.jinja_env.globals['get_locale'] = get_locale

@app.context_processor
def utility_processor():
    return dict(get_locale=get_locale)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def fetch_threats_background():
    while True:
        with app.app_context():
            try:
                phishtank_api_key = os.environ.get('PHISHTANK_API_KEY', 'your_phishtank_api_key')
                phishtank_url = f'http://data.phishtank.com/data/{phishtank_api_key}/online-valid.json'
                response = requests.get(phishtank_url)
                if response.status_code == 200:
                    phishing_data = response.json()
                    for entry in phishing_data[:5]:
                        url = entry.get('url')
                        if not Threat.query.filter_by(details=url).first():
                            new_threat = Threat(
                                type='Phishing',
                                severity='High',
                                ip_address=None,
                                source='PhishTank',
                                details=url
                            )
                            db.session.add(new_threat)
                            db.session.commit()
                            socketio.emit('new_threat', {
                                'id': new_threat.id,
                                'type': new_threat.type,
                                'severity': new_threat.severity,
                                'timestamp': new_threat.timestamp.isoformat(),
                                'details': new_threat.details
                            }, namespace='/dashboard')

                vt_api_key = os.environ.get('VIRUSTOTAL_API_KEY', 'your_virustotal_api_key')
                vt_url = 'https://www.virustotal.com/api/v3/files'
                headers = {'x-apikey': vt_api_key}
                file_hash = 'd41d8cd98f00b204e9800998ecf8427e'
                response = requests.get(f'{vt_url}/{file_hash}', headers=headers)
                if response.status_code == 200:
                    vt_data = response.json()
                    if vt_data['data']['attributes']['last_analysis_stats']['malicious'] > 0:
                        if not Threat.query.filter_by(details=file_hash).first():
                            new_threat = Threat(
                                type='Malware',
                                severity='High',
                                ip_address=None,
                                source='VirusTotal',
                                details=file_hash
                            )
                            db.session.add(new_threat)
                            db.session.commit()
                            socketio.emit('new_threat', {
                                'id': new_threat.id,
                                'type': new_threat.type,
                                'severity': new_threat.severity,
                                'timestamp': new_threat.timestamp.isoformat(),
                                'details': new_threat.details
                            }, namespace='/dashboard')
            except Exception as e:
                logging.error(f"Error fetching threats: {e}")
        time.sleep(300)

thread = Thread(target=fetch_threats_background)
thread.daemon = True
thread.start()

from routes.auth import auth_bp
from routes.home import home_bp
from routes.quiz import quiz_bp
from routes.report import report_bp
from routes.api import api_bp
from routes.feedback import feedback_bp
from routes.privacy import privacy_bp
from routes.admin import admin_bp
from routes.phishing import phishing_bp
from routes.password_strength import password_strength_bp
from routes.password_generator import password_generator_bp
from routes.breach_checker import breach_checker_bp
from routes.malware_scanner import malware_scanner_bp
from routes.dashboard import dashboard_bp
from routes.otp import otp_bp

app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(quiz_bp)
app.register_blueprint(report_bp)
app.register_blueprint(api_bp)
app.register_blueprint(feedback_bp)
app.register_blueprint(privacy_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(phishing_bp)
app.register_blueprint(password_strength_bp)
app.register_blueprint(password_generator_bp)
app.register_blueprint(breach_checker_bp)
app.register_blueprint(malware_scanner_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(otp_bp)
       # Exempt auth routes from CSRF for development
csrf.exempt(auth_bp)

@app.route('/set-theme', methods=['POST'])
@csrf.exempt
def set_theme():
    data = request.get_json()
    theme = data.get('theme', 'light')
    session['theme'] = theme
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    with app.app_context():
        logging.debug("Creating all database tables")
        try:
            db.create_all()
            logging.debug("Database tables created successfully")
        except Exception as e:
            logging.error(f"Error creating tables: {e}")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)