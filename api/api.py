from playhouse.shortcuts import model_to_dict
from flask import Blueprint, jsonify
import models
import requests

# api = Blueprint("api", "api", url_prefix="/api/v1")

# @api.route("/", methods=["GET"])
# def get_flicks():
#     api_key = "76b7eb9d74b21ff2bf120a4499967ac6"
#     requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query=Avengers")
