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

users_pages = Blueprint('users', __name__,
                        template_folder='Templates', static_folder='static', url_prefix="/users")

@users_pages.route("/<int:user_id>")
@login_required
def users(user_id):
    return render_template("library.html", loggedinuser = current_user.username, loggedinuserid = current_user.id)

@users_pages.route("/<int:user_id>/likes")
@login_required
def users_likes(user_id):
    liked_songs = User.find(user_id).favorite_tracks
    liked_songs_dict = [track.as_dict() for track in liked_songs]
    return render_template("likes.html", loggedinuser = current_user.username, loggedinuserid = current_user.id, liked_songs = liked_songs, liked_songs_dict = liked_songs_dict)

@users_pages.route("/<int:user_id>/library")
@login_required
def users_library(user_id):
    liked_playlists = current_user.playlists
    logging.info(liked_playlists)
    return render_template("library.html", loggedinuser = current_user.username, loggedinuserid = current_user.id, liked_playlists = liked_playlists)




