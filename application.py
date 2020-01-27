from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from models import (Workout)

# Initialize Flask app with SQLAlchemy
application = Flask(__name__)
app = application
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

@app.route('/')
def index_page():
  return "swiftshirt backend api"

@app.route('/test-data')
def test_page():
  return jsonify({
    "id" : 1,
    "name" : "Arm Day",
    "avg_hrt" : 96
  })

@app.route('/info')
def info_page():
  return "<html><head></head><body>A RESTful API in Flask using SQLAlchemy. For more info on usage, go to <a href>https://github.com/mgreenw/flask-restapi-example</a>.</body></html>"

@app.route('/api/v1/workout/<id>')
def get_workout():
  try:
    workout = Workout.query.filter_by(id=id).first()
    return jsonify(workout.serialize)
  except:
    return not_found("Workout does not exist")

# # Doctor Routes
# @app.route('/api/v1/doctors/<id>')
# def show_doctor(id):
#   try:
#     doctor = Doctor.query.filter_by(id=id).first()
#     return jsonify(doctor.serialize)
#   except:
#     return not_found("Doctor does not exist")


# @app.route('/api/v1/doctors', methods=['POST'])
# def create_doctor():
#   if not request.is_json or 'name' not in request.get_json():
#     return bad_request('Missing required data.')
#   doctor = Doctor(request.get_json()['name'])
#   db.session.add(doctor)
#   db.session.commit()
#   return jsonify({'doctor': doctor.serialize}), 201

# #Review Routes
# @app.route('/api/v1/reviews/<id>')
# def show_review(id):
#   try:
#     review = Review.query.filter_by(id=id).first_or_404()
#     return jsonify(id=review.id,
#              doctor_id=review.doctor_id,
#              description=review.description,
#              doctor=dict(id=review.doctor.id,
#                    name=review.doctor.name))
#   except:
#     return not_found("Review does not exist.")

# @app.route('/api/v1/reviews', methods=['POST'])
# def create_review():
#   request_json = request.get_json()
#   if not request.is_json or 'doctor_id' not in request_json or 'description' not in request_json:
#     return bad_request('Missing required data.')
#   doctor_id = request_json['doctor_id']

#   # If the doctor_id is invalid, generate the appropriate 400 message
#   try:
#     review = Review(doctor_id=doctor_id, description=request_json['description'])
#     db.session.add(review)
#     db.session.commit()
#   except:
#     return bad_request('Given doctor_id does not exist.')
#   return jsonify({'review': review.serialize}), 201


# Custom Error Helper Functions
def bad_request(message):
  response = jsonify({'error': message})
  response.status_code = 400
  return response

def not_found(message):
  response = jsonify({'error': message})
  response.status_code = 404
  return response

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)