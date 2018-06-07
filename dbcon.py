from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =  'mysql://root:''@localhost/myflaskdb'

db = SQLAlchemy(app)

class dbcon(db.Model):
    __tablename__  = 'register'
    name = db.Column('UserId', db.Integer, primary_key=True, nullable=False)
    email = db.Column('email', db.String(length=16), primary_key=True, nullable=False)
    mobile = db.Column('mobileNumber', db.Integer(), primary_key=True, nullable=False)
    username = db.Column('username', db.String(length=20))
    password = db.Column('password', db.String(length=32),nullable=False)
