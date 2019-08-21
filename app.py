from flask import Flask, g
# from api.api import api
from flask import jsonify, request
import requests
import models

DEBUG = True
PORT = 8000

app = Flask(__name__)

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
    return "Flask"

# @app.route("/", methods=["GET"])
# def get_flicks():
#     try:
#         api_key = "76b7eb9d74b21ff2bf120a4499967ac6"
#         response = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query=Avengers")
#         print(response)
#         flicks = models_to_dict(response)
#         return jsonify(data=flicks, status={"code": 200, "message": "Success"})
#     except:
#         return jsonify(data={}, status={"code": 401, "message": "There was an error retrieving your data."})


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)



# app.register_blueprint(api)