from flask_bcrypt import Bcrypt
from models import db, User, Threat, Usage, OTP, AuditLog, Scan
from app import app
from datetime import datetime, timedelta, timezone
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

bcrypt = Bcrypt()
with app.app_context():
    logging.debug("Seeding database")
    try:
        admin = User(
            username='admin',
            email='admin@cybersafe.zm',
            password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            is_admin=True,
            last_activity=datetime.now(timezone.UTC)
        )
        user = User(
            username='user1',
            email='user1@cybersafe.zm',
            password=bcrypt.generate_password_hash('user123').decode('utf-8'),
            last_activity=datetime.now(timezone.UTC)
        )
        threat = Threat(
            type='Phishing',
            severity='High',
            timestamp=datetime.now(timezone.UTC),
            details='http://malicious.com',
            source='Manual'
        )
        usage = Usage(
            user_id=1,
            action='login',
            timestamp=datetime.now(timezone.UTC)
        )
        otp = OTP(
            user_id=1,
            code='123456',
            created_at=datetime.now(timezone.UTC),
            expires_at=datetime.now(timezone.UTC) + timedelta(minutes=5)
        )
        audit_log = AuditLog(
            user_id=1,
            action='login',
            details='Admin logged in',
            timestamp=datetime.now(timezone.UTC)
        )
        scan = Scan(
            user_id=1,
            target='https://example.com',
            result='No vulnerabilities detected',
            timestamp=datetime.now(timezone.UTC)
        )
        db.session.add_all([admin, user, threat, usage, otp, audit_log, scan])
        db.session.commit()
        logging.debug("Database seeded successfully")
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error seeding database: {e}")
        sys.exit(1)