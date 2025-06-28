import sys
import logging
from app import app, db

   # Configure logging to file and console
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logging.debug("Starting database initialization")
try:
    with app.app_context():
        logging.debug("Attempting to create database tables")
        db.create_all()
        logging.debug("Database tables created successfully")
except Exception as e:
    logging.error(f"Error creating database: {e}")
    sys.exit(1)