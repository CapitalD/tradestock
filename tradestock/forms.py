from flask_wtf import Form
from wtforms import StringField, RadioField, DecimalField, SelectField
from wtforms.validators import DataRequired, NumberRange

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
    quantity = DecimalField('quantity')
    split = RadioField('split', choices=[('1', 'All'), ('2','Choose quantity'), ('3','Choose percentage')], default='1', validators=[DataRequired()])
    split_quantity = DecimalField('split_quantity', validators=[NumberRange(min=0)])
    split_percentage = DecimalField('split_percentage', default=100, validators=[NumberRange(min=0, max=100)])
