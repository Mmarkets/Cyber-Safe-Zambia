from flask import Blueprint, render_template, flash
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired
from controllers.password_controller import generate_password
from flask_login import login_required

password_generator_bp = Blueprint('password_generator', __name__)

class PasswordGeneratorForm(FlaskForm):
    length = SelectField('Password Length', choices=[(str(i), str(i)) for i in range(8, 25)], default='12', validators=[DataRequired()])
    include_symbols = SelectField('Include Symbols', choices=[('yes', 'Yes'), ('no', 'No')], default='yes', validators=[DataRequired()])
    submit = SubmitField('Generate Password')

@password_generator_bp.route('/password-generator', methods=['GET', 'POST'])
@login_required
def password_generator():
    form = PasswordGeneratorForm()
    result = None
    if form.validate_on_submit():
        length = int(form.length.data)
        include_symbols = form.include_symbols.data == 'yes'
        result = generate_password(length, include_symbols)
        flash(result['status'], result['category'])
    return render_template('password_generator.html', form=form, result=result)