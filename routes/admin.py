from flask import Blueprint, render_template, jsonify, request, abort
from flask_login import login_required, current_user
from models import db, User, AuditLog
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
def stats():
    if not current_user.is_admin:
        abort(403)
    endpoint_health = {
        'antivirus': True,
        'os_updates': False,
        'firewall': True,
        'admin_logins': True
    }
    return render_template('admin.html', endpoint_health=endpoint_health)

@admin_bp.route('/admin/users')
@login_required
def manage_users():
    if not current_user.is_admin:
        abort(403)
    return render_template('admin_users.html')

@admin_bp.route('/admin/user/<int:user_id>/ban', methods=['POST'])
@login_required
def ban_user(user_id):
    if not current_user.is_admin:
        abort(403)
    user = db.session.get(User, user_id)
    if user:
        user.banned = True
        db.session.commit()
        audit_log = AuditLog(
            user_id=current_user.id,
            action='ban_user',
            details=f'Banned user {user.username}',
            timestamp=datetime.utcnow()
        )
        db.session.add(audit_log)
        db.session.commit()
        return jsonify({'status': 'success', 'message': f'User {user.username} banned'})
    return jsonify({'status': 'error', 'message': 'User not found'}), 404

@admin_bp.route('/admin/user/<int:user_id>/unban', methods=['POST'])
@login_required
def unban_user(user_id):
    if not current_user.is_admin:
        abort(403)
    user = db.session.get(User, user_id)
    if user:
        user.banned = False
        db.session.commit()
        audit_log = AuditLog(
            user_id=current_user.id,
            action='unban_user',
            details=f'Unbanned user {user.username}',
            timestamp=datetime.utcnow()
        )
        db.session.add(audit_log)
        db.session.commit()
        return jsonify({'status': 'success', 'message': f'User {user.username} unbanned'})
    return jsonify({'status': 'error', 'message': 'User not found'}), 404

@admin_bp.route('/admin/user/<int:user_id>/role', methods=['POST'])
@login_required
def update_role(user_id):
    if not current_user.is_admin:
        abort(403)
    data = request.get_json()
    is_admin = data.get('is_admin', False)
    user = db.session.get(User, user_id)
    if user:
        user.is_admin = is_admin
        db.session.commit()
        audit_log = AuditLog(
            user_id=current_user.id,
            action='update_role',
            details=f'Updated role for user {user.username} to {"admin" if is_admin else "user"}',
            timestamp=datetime.utcnow()
        )
        db.session.add(audit_log)
        db.session.commit()
        return jsonify({'status': 'success', 'message': f'User {user.username} role updated'})
    return jsonify({'status': 'error', 'message': 'User not found'}), 404