import os
from flask import Flask
from flask import flash, render_template, request, jsonify
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_continuum import make_versioned
from datetime import datetime
import time
import logging

#from app import app

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s()] %(levelname)s %(message)s"
logger = logging.getLogger('root')
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)

app = Flask(__name__)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "person.db"))

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config["DEBUG"] = True

db = SQLAlchemy(app)
make_versioned(user_cls=None)


class Person(db.Model):
    __versioned__ = {}
    __tablename__ = 'tbl_person'

    userId = db.Column(db.String(20), primary_key=True)
    firstName = db.Column(db.String(70), nullable=False)
    middleName = db.Column(db.String(70), nullable=True)
    lastName = db.Column(db.String(70), nullable=False)
    email = db.Column(db.String(70), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __init__(self, userId, firstName, middleName, lastName, email, age):
        self.userId = userId
        self.firstName = firstName
        self.middleName = middleName
        self.lastName = lastName
        self.email = email
        self.age = age

sqlalchemy.orm.configure_mappers()

@app.route('/')
@app.route('/noyo/')
@app.route('/noyo/person/')
def home_page():
    return render_template('create.html')

@app.route('/noyo/person/', methods=['POST'])
def create_person():
    """
     Task1: Create a new person
     This function accepts person details and stores it in the DB
    """
    try:
        userId = request.form['userId']
        firstName = request.form['firstName']
        middleName = request.form['middleName']
        lastName = request.form['lastName']
        email = request.form['email']
        age = int(request.form['age'])

        person = Person(userId, firstName, middleName, lastName, email, age)

        db.session.add(person)
        db.session.commit()
        dateTimeObj = datetime.now()
        logger.info('%s Person details for user_id %s created', dateTimeObj, userId)
        return jsonify({'success':True, 'results': return_json(person)})
    except Exception as e:
        if 'UNIQUE constraint' in str(e):
            dateTimeObj = datetime.now()
            logger.exception('Exception trace: ', dateTimeObj)
            return render_template('create.html', errorMessage="Person with entered user ID already exists, please re-enter your details")
        else:
            dateTimeObj = datetime.now()
            logger.exception('Exception trace: ', dateTimeObj)

@app.route('/noyo/person/<userId>', methods=['GET'])
def fetch_person(userId):
    """
     Task2: Fetch the latest version of a single person using their id
    """
    validate = check_userId(userId)
    if validate:
        person = Person.query.get(userId)
        dateTimeObj = datetime.now()
        logger.info('%s Person details for user_id %s fetched', dateTimeObj, userId)
        return jsonify({'success':True, 'results': return_json(person)})
    return jsonify({'success':False, 'status': 400, 'message':'User ID does not exsist'})

@app.route('/noyo/person/<userId>/<int:version>', methods=['GET'])
def fetch_versioned_person(userId, version):
    """
     Task3: Fetch a single person using their id and a specified version
    """
    validate = check_userId(userId)
    if validate:
        person = Person.query.get(userId)
        validated_version = check_version(person, version)
        if validated_version:
            dateTimeObj = datetime.now()
            logger.info('%s Person details for user_id %s and version %d fetched', dateTimeObj, userId, version)
            return jsonify({'success':True, 'results': return_json(person.versions[int(version)])})
        else:
            return jsonify({'success':False,'error':'Version does not exsist'})
    return jsonify({'success':False, 'status': 400, 'message':'User Id does not exsist'})

@app.route('/noyo/all_persons', methods=['GET'])
def fetch_all():
    """
     Task4: Fetch a list of all persons (latest version)
    """
    all_persons = Person.query.all()
    dateTimeObj = datetime.now()
    logger.info('%s Latest version of people fetched', dateTimeObj)
    return jsonify({'success':True, 'results':return_json(all_persons)})

@app.route('/noyo/person/update')
def render_update():
    return render_template('update.html')

@app.route('/noyo/person/updatePerson', methods=['POST'])
def update_person():
    """
     Task5: Update a single person using their id
    """
    userId = request.form['userId']
    validate = check_userId(userId)
    if validate:
        # validate all fields for strings vs numbers
        person = Person.query.get(userId)

        person.firstName = request.form['firstName'] if (request.form['firstName'] or request.form['firstName'] != '') else person.firstName
        person.middleName = request.form['middleName'] if request.form['middleName'] or request.form['middleName'] != '' else person.middleName
        person.lastName = request.form['lastName'] if request.form['lastName'] or request.form['lastName'] != '' else person.lastName
        person.email = request.form['email'] if request.form['email'] or request.form['email'] != '' else person.email
        person.age = request.form['age'] if request.form['age'] else person.age
        db.session.commit()
        dateTimeObj = datetime.now()
        logger.info('%s Entry for User ID %s updated', dateTimeObj, userId)
        return jsonify({'success':True, 'results': return_json(person)})
    return jsonify({'success':False, 'status': 400, 'message':'User ID does not exsist, person was not updated'})

@app.route('/noyo/person/<userId>', methods=['DELETE'])
def delete_user(userId):
    """
     Task6: Delete a single person using their id
    """
    validate = check_userId(userId)
    if validate:
        person = Person.query.get(userId)
        db.session.delete(person)
        db.session.commit()
        dateTimeObj = datetime.now()
        logger.info('%s Entry for User ID %s deleted', dateTimeObj, userId)
        return jsonify({'success':True, 'results': return_json(person)})
    return jsonify({'success':False, 'status': 400, 'message':'User ID does not exsist, person was not deleted'})


def check_userId(userId):
    """
     Helper function to check for valid user ID
    """
    if userId is not None:
        person = Person.query.get(userId)
        if person:
            return True
    dateTimeObj = datetime.now()
    logger.error('%s User ID %s does not exsist', dateTimeObj, userId)
    return False


def check_version(person, version):
    """
     Helper function to check for valid version
    """
    try:
        person.versions[int(version)]
    except IndexError:
        dateTimeObj = datetime.now()
        logger.error('%s Version %d for User ID %s does not exsist', dateTimeObj, version, person.userId)
        return False
    return True

def return_json(person):
    row = []
    if isinstance(person, list):
        for p in person:
            row.append({'userId':p.userId,'firstName':p.firstName,'lastName':p.lastName,'email':p.email, 'age':p.age})
    else:
        row.append({'userId':person.userId,'firstName':person.firstName,'lastName':person.lastName,'email':person.email, 'age':person.age})
    return row

@app.errorhandler(404)
def page_not_found(error):
	dateTimeObj = datetime.now()
	logger.exception(dateTimeObj)
	return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(error):
	dateTimeObj = datetime.now()
	logger.exception(dateTimeObj)
	return render_template('500.html'),500

@app.errorhandler(405)
def method_not_allowed_error(error):
	dateTimeObj = datetime.now()
	logger.exception(dateTimeObj)
	return render_template('405.html'),405


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
