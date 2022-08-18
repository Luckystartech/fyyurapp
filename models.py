from datetime import datetime
from sqlalchemy import DateTime
# from app import *
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
import config



# app = Flask(__name__)
db = SQLAlchemy()

# migrate = Migrate(app, db)


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable = False)
    genres = db.Column("genres", db.ARRAY(db.String()), nullable = False)
    city = db.Column(db.String(120), nullable = False)
    state = db.Column(db.String(120), nullable = False)
    address = db.Column(db.String(120), nullable = False)
    phone = db.Column(db.String(120))
    website = db.Column(db.String(300))
    
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(300))
    seeking_talent = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.String(500))
    # shows = db.relationship('Show', backref='venue', lazy=True)
    shows = db.relationship('Show', backref='venue', lazy='joined', cascade="all, delete")

    def __repr__(self):
        return f"<Venue {self.id} name: {self.name}>"

    

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable = False)
    city = db.Column(db.String(120), nullable = False)
    state = db.Column(db.String(120), nullable = False)
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    genres = db.Column("genres", db.ARRAY(db.String()), nullable = False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
    # shows = db.relationship('Show', backref='artist', lazy=True)
    shows = db.relationship('Show', backref='artist', lazy='joined', cascade="all, delete")

    def __repr__(self):
        return f"<Artist {self.id} name: {self.name}>"

class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Show {self.id}, Artist {self.artist_id}, Venue {self.venue_id}>"


