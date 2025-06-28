from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from models import db, User, OTP
from flask_babel import _
from datetime import datetime, timedelta
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG)

otp_bp = Blueprint('otp', __name__)

class ResetRequestForm(FlaskForm):
    email = StringField(_('Email'), validators=[DataRequired(), Length(max=120)])
    submit = SubmitField(_('Request Password Reset'))

class ResetPasswordForm(FlaskForm):
    code = StringField(_('OTP Code'), validators=[DataRequired(), Length(min=6, max=6)])
    password = StringField(_('New Password'), validators=[DataRequired(), Length(min=6)])
    submit = SubmitField(_('Reset Password'))

@otp_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            otp = OTP(
                user_id=user.id,
                code=OTP.generate_otp(),
                expires_at=datetime.utcnow() + timedelta(minutes=10)
            )
            db.session.add(otp)
            db.session.commit()
            logging.debug(f"OTP generated for user {user.email}: {otp.code}")
            flash(_('An OTP has been sent to your email.'), 'info')
            print(f"OTP for {user.email}: {otp.code}")  # Temporary for testing
            return redirect(url_for('otp.reset_password', email=user.email))
        else:
            flash(_('Email not found.'), 'danger')
    return render_template('auth/reset_request.html', form=form)

@otp_bp.route('/reset_password/<email>', methods=['GET', 'POST'])
def reset_password(email):
    form = ResetPasswordForm()
    user = User.query.filter_by(email=email).first()
    if not user:
        flash(_('Invalid email.'), 'danger')
        return redirect(url_for('otp.reset_request'))
    if form.validate_on_submit():
        otp = OTP.query.filter_by(user_id=user.id, code=form.code.data).first()
        if otp and otp.is_valid():
            user.set_password(form.password.data)
            OTP.query.filter_by(user_id=user.id).delete()
            db.session.add(AuditLog(user_id=user.id, action='Password reset'))
            db.session.commit()
            flash(_('Password reset successful! Please log in.'), 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(_('Invalid or expired OTP.'), 'danger')
    return render_template('auth/reset_password.html', form=form, email=email)