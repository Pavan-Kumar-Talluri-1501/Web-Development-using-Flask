from flask_wtf import FlaskForm
from wtforms import StringField, IntegerRangeField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class AddOwnerForm(FlaskForm):

    name = StringField('Name of the owner: ', validators=[DataRequired()])
    pup_id = IntegerField('Puppies ID: ', validators=[DataRequired()])
    submit = SubmitField('Add Owner')