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

albums_pages = Blueprint('albums', __name__,
                        template_folder='Templates', static_folder='static', url_prefix="/albums/")

@albums_pages.route("/<int:album_id>")
def album(album_id):
    artist = Artist.find(request.args.get("artist"))
    album = Artist.get_chosen_album(artist, album_id)
    artist_dict = deepcopy(artist).as_dict()
    for track in artist_dict["tracks_top"]:
        track = eval(track)
    album_dict = deepcopy(album).as_dict()
    for track in album_dict["tracklist"]:
        track = eval(track)
    if current_user.is_anonymous:
        return render_template("album.html", artist = artist, artist_dict = artist_dict, album = album, album_dict = album_dict)
    favorite_tracks = [Track.as_dict(track) for track in current_user.favorite_tracks]
    #logging.info(favorite_tracks)
    return render_template("album.html", loggedinuser=current_user.username, artist = artist, album = album, loggedinuserid = current_user.id, favorite_tracks = favorite_tracks, artist_dict = artist_dict, album_dict = album_dict)





