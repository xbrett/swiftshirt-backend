from flask import Flask, jsonify, request, abort, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import (Workout, GenericCharacteristic)

# Initialize Flask app with SQLAlchemy
application = Flask(__name__)
app = application
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
CORS(app)

@app.route('/')
def index_page():
  return "swiftshirt backend api"

@app.route('/info')
def info_page():
  return "A RESTful API in Flask using SQLAlchemy."

@app.route('/api/v1/raw', methods=['POST'])
def post_raw():
  expected_fields = ['timestamp', 'charName', 'charValue']

  if not request.is_json or not all(field in request.get_json() for field in expected_fields):
    return bad_request('Bad or missing data.')

  try:
    charicteristic = GenericCharacteristic(
      request.get_json()['charName'], 
      request.get_json()['charValue'],
      request.get_json()['timestamp'])

    db.session.add(charicteristic)
    db.session.commit()
    return jsonify(charicteristic.serialize), 201
  except:
    return server_error("Unable to upload data")


@app.route('/api/v1/workout/<id>', methods=['GET'])
def get_workout(id):
  try:
    workout = Workout.query.filter_by(id=id).first()
    return jsonify(workout.serialize)
  except:
    return not_found("Workout does not exist")

@app.route('/api/v1/workout', methods=['POST'])
def post_workout():
  expected_fields = ['name', 'avg_hrt']

  if not request.is_json or not all(field in request.get_json() for field in expected_fields):
    return bad_request('Bad or missing data.')

  try:
    workout = Workout(
      request.get_json()['name'], 
      request.get_json()['avg_hrt'])

    db.session.add(workout)
    db.session.commit()
    return jsonify(workout.serialize), 201
  except:
    return server_error("Unable to create workout")

@app.route('/api/v1/workout/<id>', methods=['DELETE'])
def delete_workout(id):
  try:
    Workout.query.filter(Workout.id == id).delete()
    db.session.commit()
    return no_content()
  except:
    return server_error("Unable to delete workout")

# Custom Error Helper Functions
def bad_request(message):
  response = jsonify({'error': message})
  response.status_code = 400
  return response

def not_found(message):
  response = jsonify({'error': message})
  response.status_code = 404
  return response

def server_error(message):
  response = jsonify({'error': message})
  response.status_code = 500
  return response

def no_content():
  response = make_response(jsonify(''), 204)
  return response

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)