from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Boolean
import os
from flask_marshmallow import Marshmallow
from flask_jwt_extended import jwt_required, create_access_token, JWTManager

app = Flask(__name__)

# Setting up the base directory where the db should be stored.
# Here the application is kept in the same folder itself.
base_directory = os.path.abspath(os.path.dirname(__file__))

# Configuring a database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_directory, 'hospital.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuring the JWT
app.config['JWT_SECRET_KEY'] = 'APPBLOGUSINGFLASK-SUPERSECRET'  # Change this to UUID

# Initializing the database
db = SQLAlchemy(app)

# Initializing marshmallow instance
ma = Marshmallow(app)

# Initializing the web tokens
jwt = JWTManager(app)


# Flask CLI commands for using the database like creating the db, deleting it and testing the db using some test data
@app.cli.command('create_db')  # Here the command given inside parentheses is used in terminal to follow instructions
def db_create():
    with app.app_context():
        db.create_all()
        print('Database creation is done!!!')


@app.cli.command('delete_db')
def db_drop():
    with app.app_context():
        db.drop_all()
        print('Database is Deleted :(')


@app.cli.command('test_db')
def db_seed():
    with app.app_context():
        result_1 = CovidResult(id=789, test_result=True)
        result_2 = CovidResult(id=987, test_result=False)
        result_3 = CovidResult(id=321, test_result=False)

        # Need to add the records to the database
        db.session.add(result_1)
        db.session.add(result_2)
        db.session.add(result_3)

        test_user_1 = Patient(patients_id=321, first_name='Ravindra', last_name='Chahal', phone_num=6549873210)
        test_user_2 = Patient(patients_id=789, first_name='Rohit', last_name='Rayudu', phone_num=1234567890)
        test_user_3 = Patient(patients_id=987, first_name='Virat', last_name='Singh', phone_num=9876543210)

        db.session.add(test_user_1)
        db.session.add(test_user_2)
        db.session.add(test_user_3)

        # After adding the records, need to save the changes by commiting it, otherwise db will be running but nothing will be seen inside database
        db.session.commit()
        print('Database Seeded')


@app.route('/')
def greet():
    return 'hello world'


@app.route('/sample_page')
def sample_page():
    # return 'Back to home'
    # explicitly specifying the status code, but it is optional
    return jsonify(message='Back to Home'), 200


@app.route('/not found')
def not_found():
    return jsonify(message='Page not found'), 404


# pass the parameters to the endpoint from the frontend directly or test the api using postman
@app.route('/param')
def parameters():
    name = request.args.get("name")
    age = int(request.args.get('age'))
    if age > 18:
        return jsonify(message="Mr." + name.capitalize() + ", You're eligible to vote."), 200
    else:
        return jsonify(message="Sorry Mr." + name.capitalize() + " You're not old enough for participating"), 401


# pass the URL parameters as arguments instead of using the request
@app.route('/url_var/<string:name>/<int:age>')
def url_variables(name: str, age: int):
    if age > 18:
        return jsonify(message="Mr." + name.capitalize() + ", You're eligible to vote."), 200
    else:
        return jsonify(message="Sorry Mr." + name.capitalize() + " You're not old enough for participating"), 401


# Retrieving the list of patients from the database
# so to this rule "methods" are added so that whatever specified inside methods like GET or POST etc. only they are accepted other methods will throw error
@app.route('/patients', methods=['GET'])
def patients():
    list_of_patients = Patient.query.all()
    # return jsonify(data = list_of_patients) # returns a typeerror saying TypeError: Object of type Patient is not JSON serializable. To do this use "Marshmallow"
    result = patients_schema.dump(list_of_patients)
    return jsonify(result)


# Creating database models
# The hospital db contains data of patients and covid Results of the patients


# Table for patients
class Patient(db.Model):
    __tablename__ = 'patients'  # It sets the table name when it generates the table, here the table name is "patients"
    patients_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_num = Column(Integer, unique=True)


# table for covid result
class CovidResult(db.Model):
    __tablename__ = 'covid_results'
    id = Column(Integer, primary_key=True)
    test_result = Column(Boolean)


# Creating Schemas using marshmallow instances
class PatientSchema(ma.Schema):
    class Meta:
        fields = ('patients_id', 'first_name', 'last_name', 'phone_num')


class ResultSchema(ma.Schema):
    class Meta:
        fields = ('id', 'test_result')


patient_schema = PatientSchema()
patients_schema = PatientSchema(
    many=True)  # Here two schemas are created because if there is only one entry it can deserialize using patient_schema, if more entries it can use patients_schema

result_schema = ResultSchema()
results_schema = ResultSchema(many=True)


# User Registration
@app.route('/registration', methods=['POST'])
def registration():
    # Assume that that calling routes using the HTML forms
    # Registration is in the form format, now we need to give the fields to register the user
    phone_num = request.form['phone_num']  # grabbing the phone number from the submitted form

    # See whether the user is already registered or not
    test = Patient.query.filter_by(
        phone_num=phone_num).first()  # this is going to call the database and will be looking for the single user with the phone number that is just passed in
    if test:
        return jsonify(message='The patient with phone number already exist')
    else:
        fname = request.form['first_name']
        lname = request.form['last_name']
        pid = request.form['patients_id']
        patient = Patient(patients_id=pid, first_name=fname, last_name=lname, phone_num=phone_num)
        db.session.add(patient)
        db.session.commit()
        return jsonify(message='Patient Registration successful'), 201  # the status code in 200s means it is successful


@app.route('/login', methods=[
    'POST'])  # The method is set to POST but this is controversial because POST is usually associated with creating the new records, but that is not done in login as we are dealing with existing users.
def login():
    if request.is_json:  # If the request is a json then grab the phone number and patients name
        phone_no = request.json['phone_num']
    else:
        phone_no = request.form['phone_num']

    test_patient = Patient.query.filter_by(
        phone_num=phone_no).first()  # checking whether there is a match by phone number
    if test_patient:  # if the patient is logged in then give the web token
        access_token = create_access_token(
            identity=phone_no)  # identity means, how the user/patient is being identified. Here they are identified using phone number
        return jsonify(message='Login Succeeded', access_token=access_token)
    else:
        return jsonify(message='Login Failed'), 401  # 401 status code means permission denied


# CRUD operations
@app.route('/patient_details/<int:patient_id>', methods=['GET'])
def patient_details(patient_id):
    patient = Patient.query.filter_by(patients_id=patient_id).first()
    if patient:
        result = patient_schema.dump(patient)
        return jsonify(result)
    else:
        return jsonify(message='Patient not found'), 404


@app.route('/add_patient', methods=['POST'])
@jwt_required()
def add_patient():
    phone_num = request.form['phone_num']  # grabbing the phone number from the submitted form

    # See whether the user is already registered or not
    test = Patient.query.filter_by(
        phone_num=phone_num).first()  # this is going to call the database and will be looking for the single user with the phone number that is just passed in
    if test:
        return jsonify(message='The patient with phone number already exist')
    else:
        fname = request.form['first_name']
        lname = request.form['last_name']
        pid = request.form['patients_id']
        patient = Patient(patients_id=pid, first_name=fname, last_name=lname, phone_num=phone_num)
        db.session.add(patient)
        db.session.commit()
        return jsonify(message='Patient Registration successful'), 201


if __name__ == "__main__":
    app.run(debug=True)
