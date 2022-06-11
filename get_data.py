import requests
from log_config import logging
from types import SimpleNamespace
from subsidiary_functions import *
import json
# from artist import Artist
# from track import Track
from db_models import *
#from mongo_collections import DatabaseAtlas

from deezer_api import DeezerData

API_KEY = "feb2a85f7ecc51b83eebf88aff3e209d"
WEBSITE = "http://ws.audioscrobbler.com"

def get_artist(id):
    artist_data = SimpleNamespace(**DeezerData.find_artist(id).json())
    artist_data.tracks_top = DeezerData.find_top(id).json()
    #for track in artist_data.tracks_top["data"]:
        #logging.info(track["album"]["cover_big"])
    artist_data.albums = DeezerData.find_albums(id).json()
    Artist1 = Artist(artist_data)
    logging.info(Artist)
    Artist.insert_one(Artist1)
    #DatabaseAtlas.insertOne("deezer_artists", Artist(artist_data).get_mongo_encoding())
    return Artist(artist_data)

# Artist.delete_all()
# #get_artist(artists[0]["id"])
# for artist in artists:
#     if artists.index(artist) > 6:
#         get_artist(artist["id"])
#DatabaseAtlas.dropCol("deezer_artists")
#artists = [get_artist(artist["id"]) for artist in artists]
#Artist.delete_all()
artists = Artist.find_all()
# all_playlists = []
# for artist in artists:
#     for playlist in artist.playlists:
#         logging.info(playlist)
#         Playlist.insert_one(playlist)
        #all_playlists.append(playlist)
    #all_playlists.append(playlist for playlist in artist.playlists)
#logging.info(all_playlists)
#artists = [artist for artist in DatabaseAtlas.findAll("deezer_artists", {})]
logging.info(artists)

        #['David Bowie', 'Coldplay', 'Radiohead', 'Queen', 'The Rolling Stones', 'The Beatles', 'Muse', 'Daft Punk', 'The Cure', 'Red Hot Chili Peppers', 'The Weeknd', 'Arctic Monkeys', 'Nirvana', 'Ed Sheeran', 'Blur', 'Pink Floyd', 'Sia', 'Bob Dylan', 'Adele', 'U2',
#  'Michael Jackson', 'The Strokes', 'Tame Impala', 'R.E.M.', 'Depeche Mode', 'Calvin Harris', 'The Killers', 'Led Zeppelin', 'Arcade Fire', 'Lana Del Rey', 'Foo Fighters', 'Imagine Dragons', 'Oasis', 'The Black Keys', 'Rihanna', 'The xx', 'Major Lazer', 'Gorillaz', 'Th
# e Clash', 'The Smiths', 'Pixies', 'Florence + the Machine', 'Fleetwood Mac', 'David Guetta', 'The White Stripes', 'Franz Ferdinand', 'Beck', 'New Order', 'Metallica', 'Vetusta Morla']



