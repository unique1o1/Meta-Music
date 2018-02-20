from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

import datetime
import json
db = SQLAlchemy()


class fetcher_database(db.Model):
    __tablename__ = 'fetcher'
    uid = db.Column('id', db.Integer, primary_key=True)
    trackname = db.Column('trackname', db.Integer)
    tracknumber = db.Column('tracknumber', db.Integer)
    image_url = db.Column('image_url', db.Text)
    artistname = db.Column('artistname', db.String(50))
    albumname = db.Column('albumname', db.String(50))

    releasedate = db.Column('releasedate', db.Integer)
    genre = db.Column('genre', db.String(50))
