import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'pets.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Puppy(db.Model):
    __tablename__ = 'puppies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # ONE-TO-MANY RELATIONSHIP
    toys = db.relationship('Toys', backref='puppy', lazy='dynamic')

    # ON-TO-ONE RELATIONSHIP
    owner = db.relationship('Owner', backref='puppy', uselist=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        if self.owner:
            return f"Puppy name is {self.name}, and owner is {self.owner.name}"
        else:
            return f"Puppy name is {self.name} and need to be purchased"

    def report_toys(self):
        print("Here are the puppy toys: ")
        for toy in self.toys:
            print(toy.toy_name)


class Toys(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    toy_name = db.Column(db.String(80))
    puppy_id = db.Column(db.Integer, db.ForeignKey('puppies.id'))

    def __init__(self, toy_name, puppy_id):
        self.toy_name = toy_name
        self.puppy_id = puppy_id

class Owner(db.Model):
    __tablename__ = 'owners'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    puppy_id = db.Column(db.Integer, db.ForeignKey('puppies.id'))

    def __init__(self, name, puppy_id):
        self.name = name
        self.puppy_id = puppy_id
