from flask_wtf import Form
from wtforms import StringField, RadioField, DecimalField, SelectField
from wtforms.validators import DataRequired

class NewJobForm(Form):
    name = StringField('name', validators=[DataRequired()])
    active = RadioField('active', choices=[('True', 'Active'), ('False', 'Inactive')], default='True', validators=[DataRequired()])

class NewStockForm(Form):
    sku = StringField('sku')
    name = StringField('name', validators=[DataRequired()])
    unitprice = DecimalField('unitprice', places=2)
    quantity = DecimalField('quantity')
    job = SelectField('job', coerce=int)

class AllocateStockForm(Form):
    job = SelectField('job', coerce=int, validators=[DataRequired()])
