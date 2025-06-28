from flask import Blueprint, render_template, flash
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
import bleach
from flask_login import login_required

feedback_bp = Blueprint('feedback', __name__)

class FeedbackForm(FlaskForm):
    feedback = TextAreaField('Your Feedback', validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField('Submit Feedback')

@feedback_bp.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        clean_feedback = bleach.clean(form.feedback.data)
        with open('feedback.txt', 'a') as f:
            f.write(f"{form.feedback.data}\n{'-'*50}\n")
        flash('Thank you for your feedback!', 'success')
    return render_template('feedback.html', form=form)