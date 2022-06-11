from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, Blueprint
from mongo_collections import DatabaseAtlas
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from db_models import *
from log_config import logging
from datetime import datetime
from subsidiary_functions import *
from get_data import artists
from copy import deepcopy
import requests
from types import SimpleNamespace
from routing.routes import index_pages
from routing.routes_artists import artists_pages
from routing.routes_artist import artist_pages
from routing.routes_playlists import playlists_pages
from routing.routes_albums import albums_pages
from routing.routes_users import users_pages
from routing.routes_login import login_pages
from routing.routes_register import register_pages
from routing.routes_logout import logout_pages
from routing.routes_api import api_pages

import datetime

app.register_blueprint(index_pages)
app.register_blueprint(artists_pages)
app.register_blueprint(artist_pages)
app.register_blueprint(playlists_pages)
app.register_blueprint(albums_pages)
app.register_blueprint(users_pages)
app.register_blueprint(login_pages)
app.register_blueprint(register_pages)
app.register_blueprint(logout_pages)
app.register_blueprint(api_pages)

if __name__ == "__main__":
    app.run(debug = True)

