#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

'''
Local Testing
'''
database_name = "fyyur"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

# database_path = "postgres://wxycixvjwwjzsl:7f2659d7263bd5d687fff5db7355ab07651877c93337e700db7d6a5052812c77@ec2-18-214-119-135.compute-1.amazonaws.com:5432/d7qolmeaeeobq6"

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    return db

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))

    shows = db.relationship('Show', backref='Venue', lazy=True)

    '''
    short()
        short form representation of the venue
    '''
    def short(self):
    	return {
    		'id': self.id,
    		'name': self.name,
    		'genres': self.genres
    	}

    '''
    long()
        long form representation of the venue
    '''
    def long(self):
    	return {
    		'id': self.id,
    		'name': self.name,
    		'genres': self.genres,
    		'city': self.city,
    		'state': self.state,
    		'address': self.address,
    		'phone': self.phone,
    		'website': self.website,
    		'image_link': self.image_link,
    		'facebook_link': self.facebook_link,
    		'seeking_talent': self.seeking_talent,
    		'seeking_description': self.seeking_description
    	}

    def insert(self):
    	db.session.add(self)
    	db.session.commit()

    def delete(self):
    	db.session.delete(self)
    	db.session.commit()

    def update(self):
    	db.session.commit()

    def __repr__(self):
    	return f'<Venue {self.id} {self.name}>'

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))

    shows = db.relationship('Show', backref='Artist', lazy=True)

    '''
    short()
        short form representation of the venue
    '''
    def short(self):
    	return {
    		'id': self.id,
    		'name': self.name,
    		'genres': self.genres
    	}

    '''
    long()
        long form representation of the venue
    '''
    def long(self):
    	return {
    		'id': self.id,
    		'name': self.name,
    		'genres': self.genres,
    		'city': self.city,
    		'state': self.state,
    		'phone': self.phone,
    		'website': self.website,
    		'image_link': self.image_link,
    		'facebook_link': self.facebook_link,
    		'seeking_venue': self.seeking_venue,
    		'seeking_description': self.seeking_description
    	}

    def insert(self):
    	db.session.add(self)
    	db.session.commit()

    def delete(self):
    	db.session.delete(self)
    	db.session.commit()

    def update(self):
    	db.session.commit()

    def __repr__(self):
    	return f'<Artist {self.id} {self.name}>'

class Show(db.Model):
	__tablename__ = 'Show'

	id = db.Column(db.Integer, primary_key=True)
	start_time =db.Column(db.DateTime, nullable=False)
	venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
	artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)

	def format(self):
		return {
			'id': self.id,
			'start_time': self.start_time,
			'venue_id': self.venue_id,
			'artist_id': self.artist_id
		}

	def insert(self):
		db.session.add(self)
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def update(self):
		db.session.commit()