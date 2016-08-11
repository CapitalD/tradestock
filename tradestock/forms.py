from flask_wtf import Form
from wtforms import StringField, RadioField
from wtforms.validators import DataRequired

class NewJobForm(Form):
    name = StringField('name', validators=[DataRequired()])
    active = RadioField('active', choices=[('True', 'Active'), ('False', 'Inactive')], default='True', validators=[DataRequired()])
