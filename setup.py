from application import application
from models import db

with application.app_context():
  db.create_all()