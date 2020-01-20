from flask import Flask
from flask_restful import Api as FlaskRestfulApi
from api.models.todo import Todo, TodoList

class Api:
  api = None
  
  def __init__(self, app):
    self.api = FlaskRestfulApi(app)
    self.add_resources()

  def add_resources(self):
    self.api.add_resource(TodoList, '/todos')
    self.api.add_resource(Todo, '/todos/<todo_id>')

