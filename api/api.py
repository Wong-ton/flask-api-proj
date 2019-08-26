import models
from playhouse.shortcuts import model_to_dict
from flask import Blueprint, jsonify, request

flick = Blueprint("flick", "flick", url_prefix="/flick/v1")


# # GET ALL FLICKS ############################################################################
@flick.route("/", methods=["GET"])
def get_all_flicks():
    try:
        flicks = [model_to_dict(flick) for flick in models.Flick.select()]
        return jsonify(data=flicks, status={"code": 200, "message" : "Data retrieved."})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message" : "There was an error retrieving the data." })


# CREATE/ADD FLICKS ######
# How would this work? 
# Need to grab flick from external API and add it to a list
# SAVE MOVIE ID


