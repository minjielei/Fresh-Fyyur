#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import os
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_cors import CORS
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from models import setup_db, Venue, Artist, Show
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
moment = Moment(app)
db = setup_db(app)

# Set up CORS, allow * for origins
CORS(app, resources={'/': {'origins': '*'}})
# Use the after_request decorator to set Access-Control-Allow
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authentication,true')
  response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,OPTIONS')
  return response

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  cities = Venue.query.distinct('city').all()
  for city in cities:
    data_entry = {}
    data_entry['city'] = city.city
    data_entry['state'] = city.state
    venues = []
    for venue in Venue.query.filter_by(city=city.city).order_by('id').all():  
      venues_entry = {}
      venues_entry['id'] = venue.id
      venues_entry['name'] = venue.name
      num_upcoming_shows = Show.query.filter(Show.venue_id==venue.id, Show.start_time>=datetime.today()).count()
      venues_entry['num_upcoming_shows'] = num_upcoming_shows
      venues.append(venues_entry.copy())
    data_entry['venues'] = venues
    data.append(data_entry.copy())

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={}
  data = []
  search_term = request.form.get('search_term', '') 
  venues = Venue.query.filter(Venue.name.ilike("%{}%".format(search_term))).all()
  response['count'] = len(venues)
  for venue in venues:
    data_entry = {}
    data_entry['id'] = venue.id
    data_entry['name'] = venue.name
    data_entry['num_upcoming_shows'] = Show.query.filter(Show.venue_id==venue.id, Show.start_time>=datetime.today()).count()
    data.append(data_entry.copy())
  response['data'] = data
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data = {}
  venue = Venue.query.filter_by(id=venue_id).one()
  data['id'] = venue.id
  data['name'] = venue.name
  data['city'] = venue.city
  data['state'] = venue.state
  data['address'] = venue.address
  data['genres'] = venue.genres
  data['phone'] = venue.phone
  data['website'] = venue.website
  data['image_link'] = venue.image_link
  data['facebook_link'] = venue.facebook_link
  data['seeking_talent'] = venue.seeking_talent
  data['seeking_description'] = venue.seeking_description

  past_shows_data = Show.query.filter(Show.venue_id==venue.id, Show.start_time < datetime.today()).all()
  past_shows = []
  upcoming_shows_data = Show.query.filter(Show.venue_id==venue.id, Show.start_time >= datetime.today()).all()
  upcoming_shows = []
  for show in past_shows_data:
    entry = {}
    entry['artist_id'] = show.artist_id
    entry['artist_name'] = Artist.query.filter_by(id=show.artist_id).one().name
    entry['artist_image_link'] = Artist.query.filter_by(id=show.artist_id).one().image_link
    entry['start_time'] = format_datetime(str(show.start_time))
    past_shows.append(entry.copy())
  for show in upcoming_shows_data:
    entry = {}
    entry['artist_id'] = show.artist_id
    entry['artist_name'] = Artist.query.filter_by(id=show.artist_id).one().name
    entry['artist_image_link'] = Artist.query.filter_by(id=show.artist_id).one().image_link
    entry['start_time'] = format_datetime(str(show.start_time))
    upcoming_shows.append(entry.copy())

  data['past_shows'] = past_shows
  data['upcoming_shows'] = upcoming_shows
  data['past_shows_count'] = len(past_shows)
  data['upcoming_shows_count'] = len(upcoming_shows)

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = VenueForm(request.form)
  if form.validate_on_submit():
    error = False
    try:
      ## get form data
      name = request.form.get('name')
      city = request.form.get('city')
      state = request.form.get('state')
      address = request.form.get('address')
      phone = request.form.get('phone')
      genres = request.form.getlist('genres')
      website = request.form.get('website')
      image_link = request.form.get('image_link')
      facebook_link = request.form.get('facebook_link')
      seeking_talent = True
      if 'seeking_talent' not in request.form:
        seeking_talent = False
      seeking_description = request.form.get('seeking_description')

      ## create a new venue record
      venue = Venue(name=name, city=city, state=state, address=address, phone=phone, genres=genres, image_link=image_link,
        facebook_link=facebook_link, website=website, seeking_talent=seeking_talent, seeking_description=seeking_description)
      db.session.add(venue)
      db.session.commit()

    # TODO: on unsuccessful db insert, flash an error instead.
    except Exception as e:
      error = True
      db.session.rollback()
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed. ' + str(e))
    finally:
      db.session.close()
      if not error:
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
  else:
    flash('Validation error. Venue ' + request.form['name'] + ' could not be listed.' + str(form.errors))
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=[]
  for artist in Artist.query.order_by('id').all():
    data_entry={}
    data_entry['id'] = artist.id
    data_entry['name'] = artist.name
    data.append(data_entry.copy())
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={}
  data = []
  search_term = request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike("%{}%".format(search_term))).all()
  response['count'] = len(artists)
  for artist in artists:
    data_entry = {}
    data_entry['id'] = artist.id
    data_entry['name'] = artist.name
    data_entry['num_upcoming_shows'] = Show.query.filter(Show.artist_id==artist.id, Show.start_time>=datetime.today()).count()
    data.append(data_entry.copy())
  response['data'] = data
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  data = {}
  artist = Artist.query.filter_by(id=artist_id).one()
  data['id'] = artist.id
  data['name'] = artist.name
  data['city'] = artist.city
  data['state'] = artist.state
  data['genres'] = ''.join(list(filter(lambda x : x!= '{' and x!='}', artist.genres ))).split(',')
  data['phone'] = artist.phone
  data['website'] = artist.website
  data['image_link'] = artist.image_link
  data['facebook_link'] = artist.facebook_link
  data['seeking_venue'] = artist.seeking_venue
  data['seeking_description'] = artist.seeking_description

  past_shows_data = Show.query.filter(Show.artist_id==artist.id, Show.start_time < datetime.today()).all()
  past_shows = []
  upcoming_shows_data = Show.query.filter(Show.artist_id==artist.id, Show.start_time >= datetime.today()).all()
  upcoming_shows = []
  for show in past_shows_data:
    entry = {}
    entry['venue_id'] = show.venue_id
    entry['venue_name'] = Venue.query.filter_by(id=show.venue_id).one().name
    entry['venue_image_link'] = Venue.query.filter_by(id=show.venue_id).one().image_link
    entry['start_time'] = format_datetime(str(show.start_time))
    past_shows.append(entry.copy())
  for show in upcoming_shows_data:
    entry = {}
    entry['venue_id'] = show.venue_id
    entry['venue_name'] = Venue.query.filter_by(id=show.venue_id).one().name
    entry['venue_image_link'] = Venue.query.filter_by(id=show.venue_id).one().image_link
    entry['start_time'] = format_datetime(str(show.start_time))
    upcoming_shows.append(entry.copy())

  data['past_shows'] = past_shows
  data['upcoming_shows'] = upcoming_shows
  data['past_shows_count'] = len(past_shows)
  data['upcoming_shows_count'] = len(upcoming_shows)

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm(request.form)
  if form.validate_on_submit():
    error = False
    try:
      ## get form data
      name = request.form.get('name')
      city = request.form.get('city')
      state = request.form.get('state')
      phone = request.form.get('phone')
      genres = request.form.getlist('genres')
      website = request.form.get('website')
      image_link = request.form.get('image_link')
      facebook_link = request.form.get('facebook_link')
      seeking_venue = True
      if 'seeking_venue' not in request.form:
        seeking_venue = False
      seeking_description = request.form.get('seeking_description')

      ## create a new venue record
      artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres, image_link=image_link,
        facebook_link=facebook_link, website=website, seeking_venue=seeking_venue, seeking_description=seeking_description)
      db.session.add(artist)
      db.session.commit()
    except Exception as e:
      error = True
      db.session.rollback()
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed. ' + str(e))
    finally:
      db.session.close()
      if not error:
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
  else:
    flash('Validation error. Artist ' + request.form['name'] + ' could not be listed.' + str(form.errors))
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[]
  for show in Show.query.order_by('start_time').all():
    data_entry = {}
    data_entry['venue_id'] = show.venue_id
    data_entry['venue_name'] = Venue.query.filter_by(id=show.venue_id).one().name
    data_entry['artist_id'] = show.artist_id
    data_entry['artist_name'] = Artist.query.filter_by(id=show.artist_id).one().name
    data_entry['artist_image_link'] = Artist.query.filter_by(id=show.artist_id).one().image_link
    data_entry['start_time'] = show.start_time.strftime("%Y-%m-%dT%H:%M:%f")
    data.append(data_entry.copy())
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False
  try:
    venue_id = request.form.get('venue_id')
    artist_id = request.form.get('artist_id')
    start_time = request.form.get("start_time")
    show = Show(venue_id=venue_id, artist_id=artist_id, start_time=start_time)
    db.session.add(show)
    db.session.commit()
  except Exception as e:
      error = True
      db.session.rollback()
      flash('An error occurred. Show could not be listed. ' + str(e))
  finally:
    db.session.close()
    if not error:
      # on successful db insert, flash success
      flash('Show was successfully listed!')
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
  