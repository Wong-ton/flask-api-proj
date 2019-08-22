import models
import os
import sys
import secrets

from flask import Blueprint, request, jsonify, url_for, send_file
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict

users = Blueprint("users", "user", url_prefix="/users")


# REGISTER ACCOUNT ######################################################################################
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
        return jsonify(data=user_dict, status={"code": 201, "success": True, "message": "Account successfully created."})


# LOGIN TO ACCOUNT ####################################################################################
@users.route("/login", methods=["POST"])
def login():
    payload = request.form.to_dict()
    payload["email"].lower()
    try:
        user = models.User.get(models.User.email == payload["email"])
        user_dict = model_to_dict(user)
        if(check_password_hash(user_dict["password"], payload["password"])):
            del user_dict["password"]
            login_user(user)
            return jsonify(data=user_dict, status={"code": 200, "success": True, "message": "Success"})
        else:
            return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})
    
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})


# EDIT USER ##########################################################################################
@users.route("/<id>", methods=["PUT"])
def edit_user(id):
    payload = request.form.to_dict()
    try:
        user = models.User.get(models.User.id == id)
        user_dict = model_to_dict(user)
        if (check_password_hash(user_dict["password"], payload["password"])):
            query = models.User.update(email = payload["email"]).where(models.User.id == id)
            query.execute()
            updated_user = models.User.get_by_id(id)
            return jsonify(data = model_to_dict(updated_user), status={"code": 200, "success": True, "message": "Success"})
        else: 
            return jsonify(data={}, status={"code": 401, "message": "An error occurred, please try again."})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "An error occurred, please try again."})


# LOGOUT & CLEAR COOKIES #############################################################################
@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")
