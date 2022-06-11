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

index_pages = Blueprint('index', __name__,
                        template_folder='Templates', static_folder='static', url_prefix="/")

@app.route("/")
def index():
    if current_user.is_anonymous:
        logging.info(artists)
        return render_template("index.html")
    return render_template("index.html", loggedinuser = current_user.username, loggedinuserid = current_user.id)





