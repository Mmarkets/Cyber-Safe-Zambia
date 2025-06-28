from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp
from flask_babel import _
import logging
from models import db, User, Usage, AuditLog
from datetime import datetime, timezone


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

class LoginForm(FlaskForm):
    email = StringField(_('Email'), validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(_('Login'))

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')
    class Meta:
        csrf = False  # Disable CSRF for form

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    from app import bcrypt
    logging.debug(f"Login request: method={request.method}, form={request.form}")
    form = LoginForm()
    if request.method == 'POST':
        logging.debug(f"Login form data: {form.data}, errors: {form.errors}")
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        logging.debug(f"User query result: {user}")
        if user and not user.banned and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            user.last_activity = datetime.now(timezone.utc)
            usage = Usage(
                user_id=user.id,
                action='login',
                timestamp=datetime.now(timezone.utc)
            )
            db.session.add(usage)
            db.session.commit()
            flash('Login successful!', 'success')
            logging.debug(f"User {user.email} logged in successfully")
            return redirect(url_for('dashboard.dashboard'))
        flash('Invalid email, password, or account banned.', 'danger')
        logging.debug(f"Login failed for {form.email.data}")
    return render_template('auth/login.html', form=form)
    

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    from app import bcrypt
    logging.debug(f"Register request: method={request.method}, form={request.form}")
    form = RegisterForm()
    if request.method == 'POST':
        logging.debug(f"Register form data: {form.data}, errors: {form.errors}")
    if form.validate_on_submit():
        if db.session.query(User).filter_by(email=form.email.data).first():
            flash('Email already registered.', 'danger')
            logging.debug(f"Registration failed: Email {form.email.data} already exists")
            return redirect(url_for('auth.register'))
        if db.session.query(User).filter_by(username=form.username.data).first():
            flash('Username already taken.', 'danger')
            logging.debug(f"Registration failed: Username {form.username.data} already exists")
            return redirect(url_for('auth.register'))
        try:
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'),
                last_activity=datetime.now(timezone.utc)
            )
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            logging.debug(f"User {user.email} registered successfully")
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}', 'danger')
            logging.error(f"Registration error: {e}")
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    current_user.last_activity = datetime.now(timezone.utc)
    usage = Usage(
        user_id=current_user.id,
        action='logout',
        timestamp=datetime.now(timezone.utc)
    )
    db.session.add(usage)
    db.session.commit()
    logout_user()
    flash('Logged out successfully.', 'success')
    logging.debug(f"User {current_user.email} logged out")
    return redirect(url_for('home.index'))