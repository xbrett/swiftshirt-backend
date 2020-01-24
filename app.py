from flask import Flask
from api.api import Api
from db.db import Db

app = Flask(__name__)

def main():
  Api(app)

  pg_config = {
    "host": "",
    "port": 5432,
    "database": "swiftshirt",
    "user": "swift"
    "password": "postgres"
  }
  db = Db(pg_config)
  app.run(debug=True)


if __name__ == '__main__':
  main()