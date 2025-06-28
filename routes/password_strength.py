from flask import Blueprint, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from controllers.password_controller import check_password_strength
from flask_login import login_required

password_strength_bp = Blueprint('password_strength', __name__)

class PasswordStrengthForm(FlaskForm):
    password = StringField('Enter Password', validators=[DataRequired()])
    submit = SubmitField('Check Strength')

@password_strength_bp.route('/password-strength', methods=['GET', 'POST'])
@login_required
def password_strength():
    form = PasswordStrengthForm()
    result = None
    if form.validate_on_submit():
        result = check_password_strength(form.password.data)
        flash(f"{result['status']}: {result['feedback']}", result['category'])
    return render_template('password_strength.html', form=form, result=result)