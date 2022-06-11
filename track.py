class Track(object):

    def __init__(self, data):
        self.id = data.id
        self.title = data.title
        self.artist = Track.find_artist(self, data)
        self.duration = data.duration
        self.explicit_lyrics = data.explicit_lyrics
        self.preview = data.preview

    def find_artist(self, data):
        if hasattr(data, "contributors"):
            return data.contributors[0]["name"]
        elif hasattr(data, "artist"):
            return data.artist["name"]

    def __str__(self):
        return self.title

    def __repr__(self):
        d = self.__dict__
        if "artist" in d:
            del d["artist"]
        if "explicit_lyrics" in d:
            del d["explicit_lyrics"]
        return str(d)