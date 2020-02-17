from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.dialects.postgresql as postgresql

db = SQLAlchemy()

class Workout(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  avg_hrt = db.Column(db.Integer)
  
  def __init__(self, name, avg_hrt):
    self.name = name
    self.avg_hrt = avg_hrt

  @property
  def serialize(self):
    """Return object data in easily serializeable format"""
    return {
      'id': self.id,
      'name': self.name,
      'avg_hrt': self.avg_hrt
    }

class GenericCharacteristic(db.Model):
  __tablename__ = 'generic_characteristic'
  id = db.Column(db.Integer, primary_key=True)
  workout_id = db.Column(db.Integer)
  name = db.Column(db.String(50), nullable=False)
  value = db.Column(db.Integer, nullable=False)
  created_at = db.Column(postgresql.BIGINT)

  def __init__(self, workout_id, name, value, created_at):
    self.workout_id = workout_id
    self.name = name
    self.value = value
    self.created_at = created_at

  @property
  def serialize(self):
    """Return object data in easily serializeable format"""
    return {
      'id': self.id,
      'workout_id': self.workout_id,
      'name': self.name,
      'value': self.value,
      'created_at': self.created_at
    }

class WorkoutBounds(db.Model):
  __tablename__ = 'workout_bounds'
  id = db.Column(db.Integer, primary_key=True)
  start = db.Column(postgresql.BIGINT)
  end = db.Column(postgresql.BIGINT)

  def __init__(self, start):
    self.start = start

  @property
  def serialize(self):
    """Return object data in easily serializeable format"""
    return {
      'id': self.id,
      'start': self.start,
      'end': self.end
    }
