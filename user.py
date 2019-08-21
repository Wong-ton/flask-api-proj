import models
import os
import sys
import secrets

from flask import Blueprint, request, jsonify, url_for, send_file
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict

users = Blueprint("users", "user", url_prefix="/users")

@users.route("/register", methods=["POST"])
def register():
    payload = request.form.to_dict()
    payload["email"].lower()

    print(payload)
    
    try:
        models.User.get(models.User.email == payload["email"])
        return jsonify(data={}, status={"code": 401, "message": "A user with that e-mail already exists."})
    
    except models.DoesNotExist:
        payload["password"] = generate_password_hash(payload["password"])
        user = models.User.create(**payload)
        login_user(user)
        user_dict = model_to_dict(user)

        print(user_dict)

        del user_dict["password"]
        return jsonify(data=user_dict, status={"code": 201, "message": "Account successfully created."})