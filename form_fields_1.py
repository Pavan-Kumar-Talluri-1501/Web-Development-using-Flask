# Form Fields

from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import (StringField, DateTimeField, BooleanField, SubmitField, IntegerField, SelectField, TextAreaField, RadioField)
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mykey'

class InfoForm(FlaskForm):
    breed = StringField('Specify your Dogs breed', validators=[DataRequired()])
    vaccine = BooleanField('Is the dog Vaccinated?')
    mood = RadioField('Select the dogs Mood?', choices=[('mood_one', 'Happy'), ('mood_tow', 'Angry')])
    food_choice = SelectField("What is the food giv en to the dog?", choices=[('chi', 'Chicken'), ('mut', 'Mutton'), ('fish', 'Fish')])
    feedback = TextAreaField("Please provide your valuable feedback")
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = InfoForm()
    if form.validate_on_submit():
        session['breed'] = form.breed.data
        session['vaccine'] = form.vaccine.data
        session['mood'] = form.mood.data
        session['food_choice'] = form.food_choice.data
        session['feedback'] = form.feedback.data

        return redirect(url_for('thankyou'))
    return render_template('fieldPractice.html', form=form)

@app.route('/thankyou')
def thankyou():
    return render_template('thanks.html')

if __name__ == '__main__':
    app.run(debug=True)