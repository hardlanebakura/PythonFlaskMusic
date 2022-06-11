from track import Track
from deezer_api import DeezerData
from types import SimpleNamespace

class Album(object):

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
        return str(self.__dict__)
