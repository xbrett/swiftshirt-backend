from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Workout(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  avg_hrt = db.Column(db.Integer)


  def __init__(self, name):
    self.name = name

  @property
  def serialize(self):
    """Return object data in easily serializeable format"""
    return {
      'id': self.id,
      'name': self.name,
      'avg_hrt': self.avg_hrt
    }

# class Doctor(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   name = db.Column(db.String(50), nullable=False)
#   reviews = db.relationship('Review', backref='doctor',
#                 lazy='select')

#   def __init__(self, name):
#     self.name = name

#   # Gets dict with the Doctor object and all of its associated reviews
#   @property
#   def serialize(self):
#     """Return object data in easily serializeable format"""
#     return {
#       'id': self.id,
#       'name': self.name,
#       'reviews': [review.serialize for review in self.reviews]
#     }

# class Review(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   description = db.Column(db.Text, nullable=False)
#   doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)

#   def __init__(self, description, doctor_id):
#     self.description = description
#     self.doctor_id = doctor_id

#   # Gets dict with the Review object
#   @property
#   def serialize(self):
#     """Return object data in easily serializeable format"""
#     return {
#       'id': self.id,
#       'doctor_id': self.doctor_id,
#       'description': self.description,
#     }