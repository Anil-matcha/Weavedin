from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
db = SQLAlchemy(app)
from routes import *
from models import *
from config import *
db.create_all()
if __name__ == '__main__':
   app.run("0.0.0.0", 8080)