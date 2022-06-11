from track import Track
from album import Album
from types import SimpleNamespace

class Artist(object):

    def __init__(self, data):
        self.name = data.name
        self.id = data.id
        self.picture = data.picture_big
        self.fans = data.nb_fan
        self.tracks_top = Artist.get_tracks_top(self, data.tracks_top["data"])
        self.albums = Artist.get_albums(self, data.albums["data"])

    def get_albums(self, data):
        return [Album(SimpleNamespace(**album)) for album in data]

    def get_tracks_top(self, data):
        return [Track(SimpleNamespace(**track)) for track in data]

    def get_tracks(self):
        return self.tracks_top

    def get_all_albums(self):
        return self.albums

    def get_mongo_encoding(self):
        #formatting class for mongodb
        d = self.__dict__
        d["tracks_top"] = [str(track.__dict__) for track in Artist.get_tracks(self)]
        d["albums"] = [str(album.__dict__) for album in Artist.get_all_albums(self)]
        return d

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self.__dict__)
