from flask_wtf import FlaskForm
from wtforms import StringField, IntegerRangeField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):
    name = StringField('Puppies name: ', validators=[DataRequired()])
    submit = SubmitField('Register')

class DeleteForm(FlaskForm):
    id = IntegerField('ID of the puppy to take home: ', validators=[DataRequired()])
    submit = SubmitField('Sent Home')