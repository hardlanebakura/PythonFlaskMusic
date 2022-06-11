from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint, abort, flash
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

logout_pages = Blueprint('logout', __name__,
                        template_folder='Templates', static_folder='static', url_prefix="/logout")

@logout_pages.route("/")
def logout():
    user = current_user.username
    logout_user()
    flash("User {} has been successfully logged out.".format(user))
    return redirect("/")





