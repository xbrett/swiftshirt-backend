from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.dialects.postgresql as postgresql


# class MyDeclarativeMeta(DeclarativeMeta):
#   def __init__(cls, name, bases, attrs):
#     bind_key = attrs.pop('__bind_key__', None)

#     DeclarativeMeta.__init__(cls, name, bases, attrs)

#     if bind_key is not None:
#       cls.__table__.info['bind_key'] = bind_key


# class Model(object):
#   @declared_attr
#   def __tablename__(cls):
#     def _join(match):
#       word = match.group()
#       if len(word) > 1:
#         return ('_%s_%s' % (word[:-1], word[-1])).lower()
#       return '_' + word.lower()
#     return _camelcase_re.sub(_join, cls.__name__).lstrip('_')


# class MySQLAlchemy(SQLAlchemy):
#   def make_declarative_base(self):
#     base = declarative_base(cls=self.BaseModel, name='Model', metaclass=self.DeclarativeMeta)
#     base.query = _QueryProperty(self)
#     return base


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
  name = db.Column(db.String(50), nullable=False)
  value = db.Column(db.Integer, nullable=False)
  created_at = db.Column(postgresql.BIGINT)

  def __init__(self, name, value, created_at):
    self.name = name
    self.value = value
    self.created_at = created_at

  @property
  def serialize(self):
    """Return object data in easily serializeable format"""
    return {
      'name': self.name,
      'value': self.value,
      #'created_at': self.created_at
    }

# class Characteristic(db.model):
#   left_bicep = db.Column(db.Integer)
#   right_bicep = db.Column(db.Integer)
#   left_forearm = db.Column(db.Integer)
#   right_forearm = db.Column(db.Integer)
#   left_chest = db.Column(db.Integer)
#   right_chest = db.Column(db.Integer)

#   left_tricep = db.Column(db.Integer)
#   right_tricep = db.Column(db.Integer)
#   left_shoulder = db.Column(db.Integer)
#   right_shoulder = db.Column(db.Integer)

#   upper_right_back = db.Column(db.Integer)
#   lower_right_back = db.Column(db.Integer)
#   upper_left_back = db.Column(db.Integer)
#   lower_left_back = db.Column(db.Integer)

#   left_ab = db.Column(db.Integer)
#   right_ab = db.Column(db.Integer)
#   created_at = db.Column(db.Timestamp)


#   def __init__(self, left_bicep, right_bicep, left_forearm, right_forearm, left_chest, right_chest, left_tricep, right_tricep,
#   left_shoulder, right_shoulder, upper_right_back, lower_right_back):
#     self.name = name
#     self.avg_hrt = avg_hrt

#   @property
#   def serialize(self):
#     """Return object data in easily serializeable format"""
#     return {
#       'id': self.id,
#       'name': self.name,
#       'avg_hrt': self.avg_hrt
#     }

  # @property
  # def deserialize(self):
  #   if not request.is_json or 'name' not in request.get_json():
  #   return bad_request('Missing required data.')
  #   return {
  #     'id': self.id,
  #     'name': self.name,
  #     'avg_hrt': self.avg_hrt
  #   }

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