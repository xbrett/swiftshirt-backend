from flask import Flask, jsonify, request, abort, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import (Workout, GenericCharacteristic, WorkoutBounds)

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
  expected_fields = ['created_at', 'name', 'value', 'workout_id']

  if not request.is_json or not all(field in request.get_json() for field in expected_fields):
    return bad_request('Bad or missing data.')

  try:
    characteristic = GenericCharacteristic(
      request.get_json()['workout_id'],
      request.get_json()['name'], 
      request.get_json()['value'],
      request.get_json()['created_at'])

    db.session.add(characteristic)
    db.session.commit()
    return jsonify(characteristic.serialize), 201
  except:
    return server_error("Unable to upload data")

@app.route('/api/v1/workout/start', methods=['POST'])
def start_workout():
  expected_fields = ['created_at']
  if not request.is_json or not all(field in request.get_json() for field in expected_fields):
    return bad_request('Bad or missing data.')

  try:
    workout = WorkoutBounds(
      request.get_json()['created_at'])

    db.session.add(workout)
    db.session.commit()
    return jsonify({"workout_id": workout.serialize.get("id")}), 201
  except:
    return server_error("Unable to upload data")

@app.route('/api/v1/workout/end', methods=['POST'])
def end_workout():
  expected_fields = ['workout_id', 'finished_at']
  if not request.is_json or not all(field in request.get_json() for field in expected_fields):
    return bad_request('Bad or missing data.')
  
  try: 
    workout_id = int(request.get_json()['workout_id'])
    workout = db.session.query(WorkoutBounds).filter_by(id=workout_id).first()
    workout.end = int(request.get_json()['finished_at'])
    db.session.commit()

    return jsonify(workout.serialize), 201
  except:
    return server_error("Unable to upload data")


@app.route('/api/v1/workouts/<id>', methods=['GET'])
def get_workout(id):
  try:
    workout = WorkoutBounds.query.filter_by(id=id).first()
    return jsonify(workout.serialize)
  except:
    return not_found("Workout not found")

@app.route('/api/v1/workouts/<id>/raw', methods=['GET'])
def get_raw_workout(id):
  expected_fields = ['offset', 'limit']
  if not request.args or not all(field in request.args for field in expected_fields):
    return bad_request('Bad or missing data.')
  
  offset = int(request.args.get('offset'))
  limit = int(request.args.get('limit'))

  try:
    raw_workout_query = GenericCharacteristic.query.filter(GenericCharacteristic.workout_id==id).order_by(GenericCharacteristic.created_at.asc()).paginate(offset, limit, False)
    total = raw_workout_query.total
    items = raw_workout_query.items
    db.session.commit()
    return paginated_results(items, total)
  except:
    return not_found("Workout data not found")


@app.route('/api/v1/workouts', methods=['GET'])
def get_all_workouts():
  expected_fields = ['offset', 'limit']
  if not request.args or not all(field in request.args for field in expected_fields):
    return bad_request('Bad or missing data.')

  offset = int(request.args.get('offset'))
  limit = int(request.args.get('limit'))
  # app.logger.info("offset: %d, limit: %d", offset, limit)

  try: 
    workout_bounds_query = WorkoutBounds.query.filter(WorkoutBounds.end != None).paginate(offset, limit, False)
    total = workout_bounds_query.total
    items = workout_bounds_query.items
    db.session.commit()

    return paginated_results(items, total)
  except:
    return not_found("Results not found")

@app.route('/api/v1/workouts', methods=['POST'])
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

def paginated_results(items, total):
  serialized_items = []
  for item in items:
    serialized_items.append(item.serialize)

  response = jsonify({'items': serialized_items, 'total': total})
  response.status_code = 200
  return response

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True, ssl_context='adhoc')