from flask_mail import Message
from flask import current_app
import logging

def send_alert_email(recipient, subject, body):
    if not current_app.config.get('MAIL_USERNAME') or not current_app.config.get('MAIL_PASSWORD'):
        logging.warning("Email configuration incomplete; skipping email send")
        return False
    try:
        msg = Message(subject, recipients=[recipient])
        msg.body = body
        current_app.extensions['mail'].send(msg)
        logging.info(f"Email sent to {recipient}: {subject}")
        return True
    except Exception as e:
        logging.error(f"Email sending error: {str(e)}")
        return False