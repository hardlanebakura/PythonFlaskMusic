from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint, abort
from jinja2 import TemplateNotFound
from log_config import logging
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from operator import itemgetter
import json
from db_models import *
import math
import random
from db_models import *
from subsidiary_functions import *
from get_data import artists
from copy import deepcopy
from types import SimpleNamespace

register_pages = Blueprint('register', __name__,
                        template_folder='Templates', static_folder='static', url_prefix="/register")

@register_pages.route('/', methods = ["POST"])
def register_post():
    email = request.form["register_email"]
    username = request.form["register_username"]
    password = request.form["register_password1"]
    nu = User(email=email, username=username, password=password)
    if not User.exists(nu):
        User.insert_one(nu)
        login_user(nu)

    return redirect("/")

@register_pages.route('/')
def register():
    all_users = User.find_all()
    return render_template("register.html", all_users=all_users)





