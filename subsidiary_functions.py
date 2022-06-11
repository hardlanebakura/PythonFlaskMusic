from create_app import create_app
from log_config import logging
import json

app = create_app()

artists_file = open("data/artists.json", encoding = "utf8")
artists = json.load(artists_file)["artists"]

def find_artist(id):
    for artist in artists:
        if artist["id"] == id:
            return artist
    return {"id":0}

def get_playlist_dict(playlist, playlist_dict):
    playlist_dict["tracklist"] = [track.as_dict() for track in playlist.tracklist]
    for track in playlist.tracklist:
        index = playlist.tracklist.index(track)
        playlist_dict["tracklist"][index]["artist_id"] = track.artist_id
        playlist_dict["tracklist"][index]["artist_name"] = track.artist_name
    return playlist_dict

def get_artist_dict(artist_dict):
    for track in artist_dict["tracks_top"]:
        track = eval(track)
    for album in artist_dict["albums"]:
        album = eval(album)
    return artist_dict

find_artist("The Clash")