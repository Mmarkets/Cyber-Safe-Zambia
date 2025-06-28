from flask import Blueprint, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from controllers.breach_controller import check_breach
from flask_login import login_required

breach_checker_bp = Blueprint('breach_checker', __name__)

class BreachForm(FlaskForm):
    email = StringField('Enter Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Check Breach')

@breach_checker_bp.route('/breach-checker', methods=['GET', 'POST'])
@login_required
def breach_checker():
    form = BreachForm()
    result = None
    if form.validate_on_submit():
        result = check_breach(form.email.data)
        flash(result['status'], result['category'])
    return render_template('breach_checker.html', form=form, result=result)