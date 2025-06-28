from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()

try:
    from models import User, Threat, Usage, OTP, AuditLog, Scan
    logging.debug("Successfully imported models")
except Exception as e:
    logging.error(f"Error importing models: {e}")
    sys.exit(1)

db.init_app(app)

with app.app_context():
    logging.debug("Attempting to create database tables")
    try:
        db.create_all()
        logging.debug("Database tables created successfully")
    except Exception as e:
        logging.error(f"Error creating tables: {e}")
        sys.exit(1)