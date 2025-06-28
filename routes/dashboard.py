from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask_socketio import emit
from models import db, Threat, User, Usage
from datetime import datetime, timedelta
from sqlalchemy.sql import func


dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    time_threshold = datetime.utcnow() - timedelta(hours=24)
    active_threats = db.session.query(func.count(Threat.id)).filter(
        Threat.resolved == False,
        Threat.timestamp >= time_threshold
    ).scalar() or 0
    compliance_percent = 85
    active_users = db.session.query(func.count(User.id)).filter(User.banned == False).scalar() or 0
    recent_usage = db.session.query(Usage).filter(
        Usage.timestamp >= time_threshold
    ).count() or 0
    endpoint_health = {
        'antivirus': True,
        'os_updates': False,
        'firewall': True,
        'admin_logins': True
    }
    return render_template('dashboard.html',
                          active_threats=active_threats,
                          compliance_percent=compliance_percent,
                          active_users=active_users,
                          recent_usage=recent_usage,
                          endpoint_health=endpoint_health)

from app import socketio

@socketio.on('connect', namespace='/dashboard')
def handle_connect():
    emit('connection_response', {'data': 'Connected to dashboard'})

@socketio.on('resolve_threat', namespace='/dashboard')
@login_required
def handle_resolve_threat(data):
    threat_id = data.get('threat_id')
    threat = db.session.get(Threat, threat_id)
    if threat:
        threat.resolved = True
        db.session.commit()
        emit('threat_resolved', {'threat_id': threat_id}, broadcast=True, namespace='/dashboard')