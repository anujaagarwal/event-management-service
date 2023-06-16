from flask import Flask
from flask_sqlalchemy import SQLAlchemy     


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123anuja@localhost/template1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# from models import models
# from routes import routes