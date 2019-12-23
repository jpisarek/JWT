from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import datetime

# app
app = Flask(__name__)


# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()


# jwt token
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=60)
jwt = JWTManager(app)


# api
api = Api(app)

import views, models, resources

api.add_resource(resources.RegistrationWithGenerateToken, '/registration')
api.add_resource(resources.LoginWithGenerateToken, '/login')
api.add_resource(resources.CheckIfTokenIsExspiered, '/check')