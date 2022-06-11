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

playlists_pages = Blueprint('playlists', __name__,
                        template_folder='Templates', static_folder='static', url_prefix="/playlists/")

@playlists_pages.route("/<int:playlist_id>")
def playlist(playlist_id):
    playlist = Playlist(SimpleNamespace(**DeezerData.find_playlist(playlist_id).json()))
    playlist_dict = get_playlist_dict(playlist, playlist.as_dict())
    favorite_playlists = [str(favorite_playlist) for favorite_playlist in current_user.playlists]
    if current_user.is_anonymous:
        return render_template("playlist.html", playlist = playlist, playlist_dict = playlist_dict)
    return render_template("playlist.html", loggedinuser=current_user.username, loggedinuserid = current_user.id, playlist = playlist, playlist_dict = playlist_dict, favorite_playlists = favorite_playlists)





