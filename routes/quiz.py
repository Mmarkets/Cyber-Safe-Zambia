from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import db, Scan, Usage
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

quiz_bp = Blueprint('quiz', __name__, url_prefix='/quiz')

@quiz_bp.route('/', methods=['GET', 'POST'])
@login_required
def quiz():
    logging.debug(f"Quiz request: method={request.method}, user={current_user.email}")
    if request.method == 'POST':
        target = request.form.get('target', 'https://example.com')
        result = "Quiz scan completed"  # Placeholder for actual scan logic
        try:
            scan = Scan(
                user_id=current_user.id,
                target=target,
                result=result,
                timestamp=datetime.now(timezone.UTC)
             )
            db.session.add(scan)
            usage = Usage(
                user_id=current_user.id,
                action='quiz_scan',
                timestamp=datetime.now(timezone.UTC)
            )
            db.session.add(usage)
            db.session.commit()
            logging.debug(f"Scan saved for user {current_user.email}: target={target}")
            flash('Scan completed successfully!', 'success')
            return redirect(url_for('dashboard.dashboard'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error saving scan: {e}")
            flash(f'Scan failed: {str(e)}', 'danger')
    return render_template('quiz.html')