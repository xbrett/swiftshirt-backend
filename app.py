from flask import Flask
from api.api import Api

app = Flask(__name__)

def main():
  Api(app)
  app.run(debug=True)


if __name__ == '__main__':
  main()