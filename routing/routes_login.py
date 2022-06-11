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

login_pages = Blueprint('login', __name__,
                        template_folder='Templates', static_folder='static', url_prefix="/login")

@login_pages.route('/', methods = ["POST"])
def login_post():
    username = request.form["username_1"]
    password = request.form["password_1"]
    check_login = User.query.filter_by(username="%s" % username).first()
    if (check_login == None):
        if (current_user.is_anonymous):
            return render_template("login.html", handle=1)
    passwords_match = check_login.password == password
    if (check_login):
        if not passwords_match:
            logging.debug("Passwords didnt match")
            return render_template("login.html", handle=2)
        else:
            logging.debug("Passwords matching!")
            login_user(check_login)
            return redirect("/")
    return redirect("/")

@login_pages.route('/')
def login():
    return render_template("login.html")





