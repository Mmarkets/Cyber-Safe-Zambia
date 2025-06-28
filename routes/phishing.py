from flask import Blueprint, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from controllers.phishing_controller import check_phishing
from flask_login import login_required

phishing_bp = Blueprint('phishing', __name__)

class PhishingForm(FlaskForm):
    url = StringField('Enter URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Check URL')

@phishing_bp.route('/phishing', methods=['GET', 'POST'])
@login_required
def phishing():
    form = PhishingForm()
    result = None
    if form.validate_on_submit():
        result = check_phishing(form.url.data)
        flash(result['status'], result['category'])
    return render_template('phishing.html', form=form, result=result)