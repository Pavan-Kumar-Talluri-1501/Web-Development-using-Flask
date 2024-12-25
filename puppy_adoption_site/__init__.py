import os

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from forms import RegistrationForm, DeleteForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mykey'

dirname = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dirname, 'puppyForm.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from puppy_adoption_site.puppies.views import puppies_blueprint
from puppy_adoption_site.owners.views import owners_blueprint

# Register the blueprint

app.register_blueprint(puppies_blueprint, url_prefix='/puppies')
app.register_blueprint(owners_blueprint, url_prefix='/owners')