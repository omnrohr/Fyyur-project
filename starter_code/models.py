
"""
Obadah alahdab
Fyyur app.py - app data modeling
Python 3.9
"""

#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from sqlalchemy import Column, String, Integer, Boolean, DateTime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

db = SQLAlchemy()


def connect_db(app):
    # Connect to postgresql
    app.config.from_object('config')
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return db


class Venue(db.Model):
    """Venue database creation and data types"""
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120),
                      default='Sorry, no contact number was provided')
    image_link = db.Column(db.String(500), nullable=False,
                           default="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60")
    facebook_link = db.Column(
        db.String(120), nullable=True, default='Sorry, no Facebook page was provided')
    genres = db.Column(db.String(50))
    website = db.Column(db.String(250), nullable=True,
                        default='Sorry, no Website link was provided')
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500), nullable=True)
    shows = db.relationship('Show', backref='venue', lazy=True)


class Artist(db.Model):
    """Artist database creation and data types"""
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    city = db.Column(db.String(120), nullable=True)
    state = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.String(120), nullable=True)
    image_link = db.Column(db.String(500), nullable=False,
                           default="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80")
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(250), nullable=True,
                        default='Sorry, no Website link was provided')
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500), nullable=True)
    shows = db.relationship('Show', backref='artist', lazy=True)


class Show(db.Model):
    """
    get the data from childs classes, Artists and venue
    """
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
    start_time = db.Column(db.DateTime, nullable=False,
                           default=datetime.now())
