import os
import models
from flask import Flask, g
from flask import jsonify, request
from flask_login import LoginManager
from flask_cors import CORS
from api.user import users
# from api.api import flick


DEBUG = True
PORT = 8000

app = Flask(__name__)

login_manager = LoginManager()
app.secret_key = 'r4nd0m str1ng'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

# URL will be changed to Heroku when ready to be deployed
CORS(users, origins=["http://localhost:3000","https://boiling-peak-26000.herokuapp.com"], supports_credentials=True)
# CORS(flick, origins=["http://localhost:3000","https://boiling-peak-26000.herokuapp.com"], supports_credentials=True)

app.register_blueprint(users)
# app.register_blueprint(flick)

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the database after each request."""
    g.db.close()
    return response

@app.route('/')
def index():
    return "This is Flask"

if 'ON_HEROKU' in os.environ:
    print('hitting')
    models.initialize()

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)


