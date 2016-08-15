from flask_wtf import Form
from wtforms import StringField, RadioField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional

class OptionalIfFieldEqualTo(Optional):
    # a validator which makes a field optional if
    # another field has a desired value

    def __init__(self, other_field_name, value, *args, **kwargs):
        self.other_field_name = other_field_name
        self.value = value
        super(OptionalIfFieldEqualTo, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if other_field.data == self.value:
            super(OptionalIfFieldEqualTo, self).__call__(form, field)

class NewJobForm(Form):
    name = StringField('name', validators=[DataRequired()])
    active = RadioField('active', choices=[('True', 'Active'), ('False', 'Inactive')], default='True', validators=[DataRequired()])

class NewStockForm(Form):
    sku = StringField('sku')
    name = StringField('name', validators=[DataRequired()])
    unitprice = DecimalField('unitprice', places=2, validators=[DataRequired()])
    quantity = DecimalField('quantity', validators=[DataRequired()])
    job = SelectField('job', coerce=int)

class AllocateStockForm(Form):
    job = SelectField('job', coerce=int, validators=[DataRequired()])
    quantity = DecimalField('quantity')
    split = RadioField('split', choices=[('1', 'All'), ('2','Choose quantity'), ('3','Choose percentage')], default='1', validators=[DataRequired()])
    split_quantity = DecimalField('split_quantity', validators=[NumberRange(min=0), OptionalIfFieldEqualTo('split', '1'), OptionalIfFieldEqualTo('split', '3')])
    split_percentage = DecimalField('split_percentage', validators=[NumberRange(min=0, max=100), OptionalIfFieldEqualTo('split', '1'), OptionalIfFieldEqualTo('split', '2')])

class WriteoffStockForm(Form):
    submit = SubmitField()
