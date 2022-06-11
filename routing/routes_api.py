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

api_pages = Blueprint('api', __name__,
                        template_folder='Templates', static_folder='static', url_prefix="/api")

@api_pages.route("/")
def api():
    return jsonify({"routes":"/api/user"})

@api_pages.route("/users/<int:user_id>")
def api_user(user_id):
    user = User.find(user_id)
    user = User.as_dict(user)
    return jsonify({"user":user})

@api_pages.route("/users/<int:user_id>/tracks", methods = ["POST"])
def api_user_add_track(user_id):
    if request.headers.get("Content-Type") == "application/json":
        user = User.find(user_id)
        track = Track(SimpleNamespace(**request.get_json()["track"]))
        user.like_track(user.username, track)
        return jsonify({"success":True, "response":"Track added"})

@api_pages.route("/users/<int:user_id>/tracks", methods = ["DELETE"])
def api_user_delete_track(user_id):
    if request.headers.get("Content-Type") == "application/json":
        user = User.find(user_id)
        track = Track(SimpleNamespace(**request.get_json()["track"]))
        for favorite_track in user.favorite_tracks:
            if favorite_track.__eq__(track):
                user.unlike_track(user.username, favorite_track)
        logging.info(user.favorite_tracks)
        return jsonify({"success":True, "response":"Track deleted"})

@api_pages.route("/users/<int:user_id>/playlists", methods = ["POST"])
def api_user_add_playlist(user_id):
    if request.headers.get("Content-Type") == "application/json":
        user = User.find(user_id)
        playlist = request.get_json()
        User.like_playlist(user.username, Playlist.find_one(playlist["id"]))
        return jsonify({"success":True, "response":"Playlist added"})

@api_pages.route("/users/<int:user_id>/playlists", methods = ["DELETE"])
def api_user_delete_playlist(user_id):
    if request.headers.get("Content-Type") == "application/json":
        user = User.find(user_id)
        playlist = Playlist.find_one(request.get_json()["id"])
        for user_playlist in user.playlists:
            if user_playlist.__eq__(playlist):
                user.unlike_playlist(user.username, user_playlist)
        return jsonify({"success":True, "response":"Playlist deleted"})

@api_pages.route("/users/<int:user_id>/albums", methods = ["POST"])
def api_user_add_album(user_id):
    if request.headers.get("Content-Type") == "application/json":
        user = User.find(user_id)
        user = User.as_dict(user)
        return jsonify({"success":True, "response":"Album added"})

@api_pages.route("/users/<int:user_id>/albums", methods = ["DELETE"])
def api_user_delete_album(user_id):
    if request.headers.get("Content-Type") == "application/json":
        user = User.find(user_id)
        user = User.as_dict(user)
        return jsonify({"success":True, "response":"Album deleted"})






