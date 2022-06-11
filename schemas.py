from marshmallow import Schema, fields
from db_models import *

class ArtistSchema(Schema):
    artist_id = fields.Int(dump_only=True)
    name = fields.Str()
    id = fields.Int
    picture = fields.Str()
    fans = fields.Str()
    tracks_top = db.Column(MutableList.as_mutable(PickleType), default=[])
    albums = db.Column(MutableList.as_mutable(PickleType), default=[])
    formatted_name = fields.Method("format_name", dump_only=True)

    def format_name(self, author):
        return "{}, {}".format(author.last, author.first)
