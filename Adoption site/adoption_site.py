import os

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import RegistrationForm, DeleteForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mykey'

dirname = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dirname, 'puppyForm.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

###############################################
############### MODELS ########################
###############################################

class Puppy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Puppy name: {self.name}"

###############################################
############ VIEW FUNCTIONS -- HAVE FORMS #####
###############################################

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def add_pup():
    form = RegistrationForm()

    if form.validate_on_submit():
        name = form.name.data
        new_pup = Puppy(name)
        db.session.add(new_pup) # or you can write in multiple lines as name = form.name.data, new_pup = Puppy(name), db.session.add(new_pup)
        db.session.commit()

        return redirect(url_for('list_of_puppies'))
    return render_template('add.html', form=form)

@app.route('/list')
def list_of_puppies():
    puppies = Puppy.query.all()
    return render_template('list.html', puppies=puppies)

@app.route('/delete', methods=['GET', 'POST'])
def delete_pup():
    form = DeleteForm()
    if form.validate_on_submit():
        id = form.id.data
        pup = db.session.get(Puppy, id)
        db.session.delete(pup)
        db.session.commit()
        return redirect(url_for('list_of_puppies'))
    return render_template('delete.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)