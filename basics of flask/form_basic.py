# Basics of WTforms

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config['SECRET_KEY'] = 'formssecretkey'

# Create a form class and pass the attributes
class InfoForm(FlaskForm):
    breed = StringField("Specify the breed of your dog")
    submit = SubmitField("Submit")

@app.route('/', methods=['GET', 'POST'])
def index():
    breed = None  # Set breed to None initially
    form = InfoForm()
    if form.validate_on_submit():
        breed = form.breed.data  # Get the data submitted in the form
        form.breed.data = ''  # Clear the input field
    return render_template('puppyForm.html', form=form, breed=breed)

if __name__ == '__main__':
    app.run(debug=True)
