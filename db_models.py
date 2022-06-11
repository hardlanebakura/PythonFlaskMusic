from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from config import db
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType
from deezer_api import DeezerData
from types import SimpleNamespace
import requests

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    datetime = db.Column(db.DateTime, default = datetime.utcnow)
    isadmin = db.Column(db.Boolean, default = False)
    favorite_tracks = db.Column(MutableList.as_mutable(PickleType), default=[])
    playlists = db.Column(MutableList.as_mutable(PickleType), default=[])

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @staticmethod
    def find(id):
        search_matches = User.query.filter_by(id = id).first()
        return search_matches

    @staticmethod
    def find_all():
        search_matches = [{"email":vars(item)["email"], "username":vars(item)["username"],  "password":vars(item)["password"], "favorite_tracks":vars(item)["favorite_tracks"], "playlists":vars(item)["playlists"], "id":vars(item)["id"]} for item in User.query.all()]
        return search_matches

    @staticmethod
    def exists(user):
        return len(db.session.query(User).filter_by(email=user.email).all()) > 0 and len(
        db.session.query(User).filter_by(username=user.username).all()) > 0

    @staticmethod
    def insert_one(user):
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def like_track(username, track):
        searched_user = User.query.filter_by(username = username).first()
        searched_user.favorite_tracks.append(track)
        db.session.commit()

    @staticmethod
    def unlike_track(username, track):
        searched_user = User.query.filter_by(username = username).first()
        searched_user.favorite_tracks.remove(track)
        db.session.commit()

    @staticmethod
    def delete_tracklist(username):
        searched_user = User.query.filter_by(username = username).first()
        searched_user.favorite_tracks.clear()
        db.session.commit()

    @staticmethod
    def like_album(username, album):
        searched_user = User.query.filter_by(username = username).first()
        db.session.commit()

    @staticmethod
    def unlike_album(username, album):
        searched_user = User.query.filter_by(username = username).first()
        db.session.commit()

    @staticmethod
    def like_playlist(username, playlist):
        searched_user = User.query.filter_by(username = username).first()
        searched_user.playlists.append(playlist)
        db.session.commit()

    @staticmethod
    def unlike_playlist(username, playlist):
        searched_user = User.query.filter_by(username = username).first()
        searched_user.playlists.remove(playlist)
        db.session.commit()

    @staticmethod
    def delete_all():
        db.session.query(User).delete()
        db.session.commit()

    @staticmethod
    def delete_one(username):
        User.query.filter_by(username = username).delete()
        db.session.commit()

    def __repr__(self):
        return "User " + str(self.id)

class Avatar(db.Model):
    __bind_key__ = "avatars"
    id = db.Column(db.Integer, primary_key=True)
    img_link = db.Column(db.String(100), nullable=False)
    img_username = db.Column(db.String(100), nullable=False, unique=True)
    datetime = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return "Avatar " + str(self.id)


class Comment(db.Model):
    __bind_key__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "Comment " + str(self.id)

class Track(db.Model):
    __bind_key__ = "tracks"
    track_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String)
    title = db.Column(db.String)
    duration = db.Column(db.Integer)
    preview = db.Column(db.String)
    cover = db.Column(db.String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @staticmethod
    def insert_one(track):
        db.session.add(track)
        db.session.commit()

    @staticmethod
    def find(id):
        search_matches = Track.query.filter_by(id = id).first()
        return search_matches

    @staticmethod
    def find_all():
        search_matches = [vars(item) for item in Track.query.all()]
        return search_matches

    @staticmethod
    def delete_all():
        db.session.query(Track).delete()
        db.session.commit()

    @staticmethod
    def delete_one(data):
        Track.query.filter_by(name = data["name"]).delete()
        db.session.commit()

    def __eq__(self, other):
        if not isinstance(other, Track):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.id == other.id and self.title == other.title

    def __init__(self, data):
        self.id = data.id
        self.title = data.title.replace("'", "")
        self.duration = data.duration
        self.preview = data.preview
        if hasattr(data, "album"):
            self.cover = data.album["cover_big"]
            self.album_id = data.album["id"]
        if hasattr(data, "artist"):
            self.artist_id = data.artist["id"]
            self.artist_name = data.artist["name"]
        if hasattr(data, "cover"):
            self.cover = data.cover
        if hasattr(data, "artist_name"):
            self.artist_name = data.artist_name

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

class Album(db.Model):
    __bind_key__ = "albums"
    album_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String)
    title = db.Column(db.String)
    cover = db.Column(db.String)
    release_date = db.Column(db.String)
    tracklist = db.Column(MutableList.as_mutable(PickleType), default=[])

    def as_dict(self):
        self.tracklist = [str(Track.as_dict(track)) for track in self.tracklist]
        d = self.__dict__
        del d["_sa_instance_state"]
        return d

    @staticmethod
    def insert_one(album):
        db.session.add(album)
        db.session.commit()

    @staticmethod
    def find_all():
        search_matches = [vars(item) for item in Album.query.all()]
        return search_matches

    @staticmethod
    def delete_all():
        db.session.query(Book).delete()
        db.session.commit()

    @staticmethod
    def delete_one(data):
        Book.query.filter_by(name = data["name"]).delete()
        db.session.commit()

    def __init__(self, data):
        self.id = data.id
        self.title = data.title
        self.cover = data.cover_big
        self.release_date = data.release_date
        self.tracklist = Album.get_tracklist(self, DeezerData.find_tracklist(data.id).json()["data"])

    def get_tracklist(self, data):
        return [Track(SimpleNamespace(**track)) for track in data]

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

class Playlist(db.Model):
    playlist_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String)
    title = db.Column(db.String)
    cover = db.Column(db.String)
    tracklist = db.Column(MutableList.as_mutable(PickleType), default=[])

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __eq__(self, other):
        if not isinstance(other, Playlist):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.id == other.id and self.title == other.title

    @staticmethod
    def insert_one(playlist):
        db.session.add(playlist)
        db.session.commit()

    @staticmethod
    def find_all():
        search_matches = [vars(item) for item in Playlist.query.all()]
        return search_matches

    @staticmethod
    def find_one(id):
        search_matches = Playlist.query.filter_by(id = id).first()
        return search_matches

    @staticmethod
    def delete_all():
        db.session.query(Playlist).delete()
        db.session.commit()

    @staticmethod
    def delete_one(data):
        Playlist.query.filter_by(name = data["name"]).delete()
        db.session.commit()

    def __init__(self, data):
        self.id = data.id
        self.title = data.title
        self.cover = data.picture_big
        self.tracklist = Playlist.get_tracklist(self, DeezerData.find_tracklist_for_playlist(data.id).json()["data"])

    def get_tracklist(self, data):
        return [Track(SimpleNamespace(**track)) for track in data]

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

class Artist(db.Model):
    __bind_key__ = "artists"
    artist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    id = db.Column(db.Integer)
    picture = db.Column(db.String)
    fans = db.Column(db.String)
    tracks_top = db.Column(MutableList.as_mutable(PickleType), default=[])
    albums = db.Column(MutableList.as_mutable(PickleType), default=[])
    playlists = db.Column(MutableList.as_mutable(PickleType), default=[])

    # def as_dict(self):
    #     d = {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def as_dict(self):
        self.tracks_top = [str(Track.as_dict(track)) for track in self.tracks_top]
        self.albums = [str(Album.as_dict(album)) for album in self.albums]
        self.playlists = [str(Playlist.as_dict(playlist)) for playlist in self.playlists]
        d = self.__dict__
        del d["_sa_instance_state"]
        return d

    @staticmethod
    def insert_one(artist):
        db.session.add(artist)
        db.session.commit()

    @staticmethod
    def find_all():
        search_matches = [item for item in Artist.query.all()]
        return search_matches

    @staticmethod
    def find(id):
        search_matches = Artist.query.filter_by(id = id).first()
        return search_matches

    @staticmethod
    def delete_all():
        db.session.query(Artist).delete()
        db.session.commit()

    @staticmethod
    def delete_one(data):
        Artist.query.filter_by(id = data["id"]).delete()
        db.session.commit()

    def get_albums(self, data):
        return [Album(SimpleNamespace(**album)) for album in data]

    def get_tracks_top(self, data):
        return [Track(SimpleNamespace(**track)) for track in data]

    def get_tracks(self):
        return self.tracks_top

    def get_all_albums(self):
        return self.albums

    def get_chosen_album(self, album_id):
        albums = Artist.get_all_albums(self)
        for album in albums:
            if album.id == album_id:
                return album

    def get_playlists(self):
        playlists = DeezerData.find_playlist_for_artist(self.id).json()["data"]
        for i, playlist in enumerate(playlists):
            playlists[i] = Playlist(SimpleNamespace(**playlist))
        return playlists

    def __init__(self, data):
        self.name = data.name
        self.id = data.id
        self.picture = data.picture_big
        self.fans = data.nb_fan
        self.tracks_top = Artist.get_tracks_top(self, data.tracks_top["data"])
        self.albums = Artist.get_albums(self, data.albums["data"])
        self.playlists = Artist.get_playlists(self)

    def __repr__(self):
        return self.name

class Book(db.Model):
    __bind_key__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(70))
    rating = db.Column(db.Integer)
    img = db.Column(db.String)
    review = db.Column(db.String)

    @staticmethod
    def insert_one(data):
        Book1 = Book(name = data["name"], author = data["author"], rating = data["rating"], img = data["img"], review = data["review"])
        db.session.add(Book1)
        db.session.commit()

    @staticmethod
    def find_all():
        search_matches = [{"name":vars(item)["name"], "author":vars(item)["author"], "rating":vars(item)["rating"], "img":vars(item)["img"], "review":vars(item)["review"]} for item in Book.query.all()]
        return search_matches

    @staticmethod
    def delete_all():
        db.session.query(Book).delete()
        db.session.commit()

    @staticmethod
    def delete_one(data):
        Book.query.filter_by(name = data["name"]).delete()
        db.session.commit()

    def __repr__(self):
        return "Book " + str(self.id)