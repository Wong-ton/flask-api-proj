import models
import os
import sys
import secrets

from flask import Blueprint, request, jsonify, url_for, send_file, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, login_required, logout_user
from playhouse.shortcuts import model_to_dict

users = Blueprint("users", "user", url_prefix="/users")


# REGISTER ACCOUNT ######################################################################################
@users.route("/register", methods=["POST"])
def register():
    # payload = request.form.to_dict()
    payload = request.get_json()
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
    payload = request.get_json()
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
    payload = request.get_json()
    try:
        user = models.User.get(models.User.id == id)
        user_dict = model_to_dict(user)
        query = models.User.update(email = payload["email"]).where(models.User.id == id)
        query.execute()
        query = models.User.update(name = payload["name"]).where(models.User.id == id)
        query.execute()
        if (check_password_hash(user_dict["password"], payload["password"]) and (payload["new_password"] == payload["confirm_password"])):
            payload["new_password"] = generate_password_hash(payload["new_password"])
            query = models.User.update(password = payload["new_password"]).where(models.User.id == id)
            query.execute()
        updated_user = models.User.get_by_id(id)

        return jsonify(data = model_to_dict(updated_user), status={"code": 200, "success": True, "message": "Success"})
        # else: 
        #     return jsonify(data = {}, status={"code": 401, "message": "An error occurred, please try again."})
    except models.DoesNotExist:
        return jsonify(data = {}, status={"code": 401, "message": "Passwords do not match."})

# can change PW be same route as edit user?
# UPDATE PASSWORD  ####################################################################################
# @users.route("/<id>/password", methods=["PUT"])
# def edit_password(id):
#     payload = request.get_json()
#     try:
#         user = models.User.get(models.User.id == id)
#         user_dict = model_to_dict(user)
#         if (check_password_hash(user_dict["password"], payload["password"]) and (payload["new_password"] == payload["confirm_password"])):
#             payload["new_password"] = generate_password_hash(payload["new_password"])
#             query = models.User.update(password = payload["new_password"]).where(models.User.id == id)
#             query.execute()
#             updated_user = models.User.get_by_id(id)

#             return jsonify(data = model_to_dict(updated_user), status={"code": 200, "success": True, "message" : "Success"})
#         else:
#             return jsonify(data={}, status={"code": 401, "message": "Passwords do not match."})
#     except models.DoesNotExist:
#         return jsonify(data={}, status={"code": 401, "message": "Invalid Username or Password"})

# HELP!
# DELETE #############################################################################
@users.route("/<id>", methods=["DELETE"])
# @login_required
def delete_user(id):
    query = models.User.delete().where(models.User.id == id)
    query.execute()
    return jsonify(data={}, status={"code": 200, "message" : "Account deleted."})
    #

# LOGOUT #######################################################################
@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")




