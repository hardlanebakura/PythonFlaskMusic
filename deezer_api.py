import requests

class DeezerData(object):

    @staticmethod
    def find_artist(id):
        return requests.get("https://api.deezer.com/artist/{}".format(id))

    @staticmethod
    def find_top(id):
        return requests.get("https://api.deezer.com/artist/{}/top".format(id))

    @staticmethod
    def find_albums(id):
        return requests.get("https://api.deezer.com/artist/{}/albums".format(id))

    @staticmethod
    def find_tracklist(album_id):
        return requests.get("https://api.deezer.com/album/{}/tracks".format(album_id))

    @staticmethod
    def find_playlist_for_artist(id):
        return requests.get("https://api.deezer.com/artist/{}/playlists".format(id))

    @staticmethod
    def find_tracklist_for_playlist(id):
        return requests.get("https://api.deezer.com/playlist/{}/tracks".format(id))

    @staticmethod
    def find_playlist(id):
        return requests.get("https://api.deezer.com/playlist/{}".format(id))