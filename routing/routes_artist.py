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

artist_pages = Blueprint('artist', __name__,
                        template_folder='Templates', static_folder='static', url_prefix="/")

@artist_pages.route("/artist/<int:artist_id>")
def artist(artist_id):
    artist = Artist.find(artist_id)
    artist_dict = get_artist_dict(deepcopy(artist).as_dict())
    if current_user.is_anonymous:
        return render_template("artist.html", artist = artist, artist_dict = artist_dict)
    favorite_tracks = [Track.as_dict(track) for track in current_user.favorite_tracks]
    return render_template("artist.html", loggedinuser=current_user.username, artist=artist, artist_dict = artist_dict, loggedinuserid = current_user.id, favorite_tracks = favorite_tracks)





