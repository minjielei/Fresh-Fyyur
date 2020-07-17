# Imports
import os
import re
import validators
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, \
    flash, redirect, url_for, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_cors import CORS
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from models import setup_db, Venue, Artist, Show
from forms import *
from auth import AuthError, requires_auth

# App Config.


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY
    moment = Moment(app)
    db = setup_db(app)
    CORS(app)

    # Filters.
    def format_datetime(value, format='medium'):
        date = dateutil.parser.parse(value)
        if format == 'full':
            format = "EEEE MMMM, d, y 'at' h:mma"
        elif format == 'medium':
            format = "EE MM, dd, y h:mma"
        return babel.dates.format_datetime(date, format)

    app.jinja_env.filters['datetime'] = format_datetime

    def is_valid_phone_number(phone):
        return re.search(r"^[0-9]{3}-[0-9]{3}-[0-9]{4}$", phone)

    def is_valid_url(url):
        return validators.url(url)

    # Controllers.
    @app.route('/')
    def index():
        return render_template('pages/login.html')

    @app.route('/home')
    def home():
        return render_template('pages/home.html')

    #  Venues
    @app.route('/venues')
    def venues():
        data = []
        cities = Venue.query.distinct('city').all()
        for city in cities:
            data_entry = {}
            data_entry['city'] = city.city
            data_entry['state'] = city.state
            venues = []
            raw_data = Venue.query.filter_by(city=city.city)\
                .order_by('id').all()
            for venue in raw_data:
                venues_entry = {}
                venues_entry['id'] = venue.id
                venues_entry['name'] = venue.name
                num_upcoming_shows = Show.query.filter(Show.venue_id == venue.id, Show.start_time >= datetime.today()).count()
                venues_entry['num_upcoming_shows'] = num_upcoming_shows
                venues.append(venues_entry.copy())
                data_entry['venues'] = venues
                data.append(data_entry.copy())

        return render_template('pages/venues.html', areas=data)

    @app.route('/venues/search', methods=['POST'])
    def search_venues():
        response = {}
        data = []
        search_term = request.form.get('search_term', '')
        venues = Venue.query.filter(Venue.name.ilike("%{}%".
                                    format(search_term))).all()
        response['count'] = len(venues)
        for venue in venues:
            data_entry = {}
            data_entry['id'] = venue.id
            data_entry['name'] = venue.name
            data_entry['num_upcoming_shows'] = Show.query.filter(Show.venue_id == venue.id,
                Show.start_time >= datetime.today()).count()
            data.append(data_entry.copy())
        response['data'] = data
        return render_template('pages/search_venues.html', results=response,
            search_term=request.form.get('search_term', ''))

    @app.route('/venues/<int:venue_id>')
    def show_venue(venue_id):
        # shows the venue page with the given venue_id
        # replace with real venue data from the venues table, using venue_id
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

        past_shows_data = Show.query.filter(Show.venue_id == venue.id,
            Show.start_time < datetime.today()).all()
        past_shows = []
        upcoming_shows_data = Show.query.filter(Show.venue_id == venue.id,
            Show.start_time >= datetime.today()).all()
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
    @app.route('/venues/create', methods=['GET'])
    # @requires_auth('post:venues')
    def create_venue_form():
        form = VenueForm()
        return render_template('forms/new_venue.html', form=form)

    @app.route('/venues/create', methods=['POST'])
    # @requires_auth('post:venues')
    def create_venue_submission():
        # insert form data as a new Venue record in the db, instead
        # modify data to be the data object returned from db insertion
        form = VenueForm(request.form)
        if form.validate_on_submit():
            error = False
            try:
                # get form data
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

                # create a new venue record
                venue = Venue(name=name, city=city, state=state, address=address, phone=phone, genres=genres, image_link=image_link,
                    facebook_link=facebook_link, website=website, seeking_talent=seeking_talent, seeking_description=seeking_description)
                db.session.add(venue)
                db.session.commit()

            # on unsuccessful db insert, flash an error instead.
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

    #  Venue APIs
    '''
    Create an endpoint to handle GET requests for venues
    '''
    @app.route('/api/venues')
    def venues_api():
        try:
            venues = [venue.short() for venue in Venue.query.order_by(Venue.id).all()]

            return jsonify({
                'success': True,
                'venues': venues,
                'total_venues': len(venues)
            })
        except Exception as e:
            abort(422)

    '''
    Create an endpoint to get venues based on a search term
    '''
    @app.route('/api/venues/search', methods=['POST'])
    def search_venues_api():
        body = request.get_json()
        search = body.get('searchTerm', None)
        try:
            venues = [venue.short() for venue in Venue.query.order_by(Venue.id).filter(Venue.name.ilike('%{}%'.format(search)))]
            return jsonify({
                'success': True,
                'venues': venues,
                'total_venues': len(venues)
            })

        except Exception as e:
            abort(422)

    '''
    Create an endpoint to POST a new venue, validating input paramters
    '''
    @app.route('/api/venues/create', methods=['POST'])
    @requires_auth('post:venues')
    def create_venues_api(payload):
        body = request.get_json()

        name = body.get('name', None)
        genres = body.get('genres', None)
        city = body.get('city', None)
        state = body.get('state', None)
        address = body.get('address', None)
        phone = body.get('phone', None)
        website = body.get('website', None)
        image_link = body.get('image_link', None)
        facebook_link = body.get('facebook_link', None)
        seeking_talent = body.get('seeking_talent', False)
        seeking_description = body.get('seeking_description', None)

        if not name or not genres or not city or not state or not address or \
            (phone and not is_valid_phone_number(phone)) or (website and not is_valid_url(website)) or \
                (image_link and not is_valid_url(image_link)) or (facebook_link and not is_valid_url(facebook_link)):
            abort(400)
        try:
            new_venue = Venue(name=name, genres=genres, city=city, state=state, address=address,
            phone=phone, website=website, image_link=image_link, facebook_link=facebook_link,
            seeking_talent=seeking_talent, seeking_description=seeking_description)
            new_venue.insert()
            venues = [venue.short() for venue in Venue.query.order_by(Venue.id).all()]
            return jsonify({
                'success': True,
                'venues': venues,
                'total_venues': len(venues)
            })

        except Exception as e:
            abort(422)

    '''
    Create a GET endpoint to get venues based on id.
    '''
    @app.route('/api/venues/<int:venue_id>')
    def show_venue_api(venue_id):
        try:
            venue = Venue.query.filter(Venue.id == venue_id).one_or_none()
            if not venue:
                abort(404)

            return jsonify({
                'success': True,
                'venue': venue.long()
            })

        except Exception as e:
            abort(422)

    '''
    Create a PATCH endpoint to edit venues based on id.
    '''
    @app.route('/api/venues/<int:venue_id>/edit', methods=['PATCH'])
    @requires_auth('patch:venues')
    def edit_venue_api(payload, venue_id):
        body = request.get_json()
        name = body.get('name', None)
        genres = body.get('genres', None)
        city = body.get('city', None)
        state = body.get('state', None)
        address = body.get('address', None)
        phone = body.get('phone', None)
        website = body.get('website', None)
        image_link = body.get('image_link', None)
        facebook_link = body.get('facebook_link', None)
        seeking_talent = body.get('seeking_talent', False)
        seeking_description = body.get('seeking_description', None)
        if not name or not genres or not city or not state or not address or \
            (phone and not is_valid_phone_number(phone)) or (website and not is_valid_url(website)) or \
                (image_link and not is_valid_url(image_link)) or (facebook_link and not is_valid_url(facebook_link)):
            abort(400)

        try:
            venue = Venue.query.filter(Venue.id == venue_id).one_or_none()
            if not venue:
                abort(404)
            venue.name = name
            venue.city = city
            venue.state = state
            venue.genres = genres
            venue.address = address
            venue.phone = phone
            venue.website = website
            venue.image_link = image_link
            venue.facebook_link = facebook_link
            venue.seeking_talent = seeking_talent
            venue.seeking_description = seeking_description

            venue.update()
            return jsonify({
                'success': True,
                'venue': venue.long()
            })

        except Exception as e:
            abort(422)

    '''
    Create a PATCH endpoint to delete venues based on id.
    '''
    @app.route('/api/venues/<venue_id>', methods=['DELETE'])
    @requires_auth('delete:venues')
    def delete_venue_api(payload, venue_id):
        try:
            venue = Venue.query.filter(Venue.id == venue_id).one_or_none()
            if not venue:
                abort(404)
            venue.delete()
            return jsonify({
                'success': True,
                'delete': venue.short()
            })

        except Exception as e:
            abort(422)

    #  Artists
    @app.route('/artists')
    def artists():
        # replace with real data returned from querying the database
        data = []
        for artist in Artist.query.order_by('id').all():
            data_entry = {}
            data_entry['id'] = artist.id
            data_entry['name'] = artist.name
            data.append(data_entry.copy())
        return render_template('pages/artists.html', artists=data)

    @app.route('/artists/search', methods=['POST'])
    def search_artists():
        # implement search on artists with partial string search. Ensure it is case-insensitive.
        # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
        # search for "band" should return "The Wild Sax Band".
        response = {}
        data = []
        search_term = request.form.get('search_term', '')
        artists = Artist.query.filter(Artist.name.ilike("%{}%".format(search_term))).all()
        response['count'] = len(artists)
        for artist in artists:
            data_entry = {}
            data_entry['id'] = artist.id
            data_entry['name'] = artist.name
            data_entry['num_upcoming_shows'] = Show.query.filter(Show.artist_id == artist.id, Show.start_time >= datetime.today()).count()
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
        data['genres'] = ''.join(list(filter(lambda x: x != '{' and x != '}', artist.genres))).split(',')
        data['phone'] = artist.phone
        data['website'] = artist.website
        data['image_link'] = artist.image_link
        data['facebook_link'] = artist.facebook_link
        data['seeking_venue'] = artist.seeking_venue
        data['seeking_description'] = artist.seeking_description

        past_shows_data = Show.query.filter(Show.artist_id == artist.id, Show.start_time < datetime.today()).all()
        past_shows = []
        upcoming_shows_data = Show.query.filter(Show.artist_id == artist.id, Show.start_time >= datetime.today()).all()
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

    #  Create Artist

    @app.route('/artists/create', methods=['GET'])
    # @requires_auth('post:artists')
    def create_artist_form():
        form = ArtistForm()
        return render_template('forms/new_artist.html', form=form)

    @app.route('/artists/create', methods=['POST'])
    # @requires_auth('post:artists')
    def create_artist_submission():
        # called upon submitting the new artist listing form
        # insert form data as a new Venue record in the db, instead
        # modify data to be the data object returned from db insertion
        form = ArtistForm(request.form)
        if form.validate_on_submit():
            error = False
            try:
                # get form data
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

                # create a new venue record
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

    #  Artist APIs
    '''
    Create an endpoint to handle GET requests for artists
    '''
    @app.route('/api/artists')
    def artists_api():
        try:
            artists = [artist.short() for artist in Artist.query.order_by(Artist.id).all()]

            return jsonify({
                'success': True,
                'artists': artists,
                'total_artists': len(artists)
            })

        except Exception as e:
            abort(422)

    '''
    Create an endpoint to get artists based on a search term
    '''
    @app.route('/api/artists/search', methods=['POST'])
    def search_artists_api():
        body = request.get_json()
        search = body.get('searchTerm', None)
        try:
            artists = [artist.short() for artist in Artist.query.order_by(Artist.id).filter(Artist.name.ilike('%{}%'.format(search)))]
            return jsonify({
                'success': True,
                'artists': artists,
                'total_artists': len(artists)
            })

        except Exception as e:
            abort(422)

    '''
    Create an endpoint to POST a new artist, validating input paramters
    '''
    @app.route('/api/artists/create', methods=['POST'])
    @requires_auth('post:artists')
    def create_artists_api(payload):
        body = request.get_json()

        name = body.get('name', None)
        genres = body.get('genres', None)
        city = body.get('city', None)
        state = body.get('state', None)
        phone = body.get('phone', None)
        website = body.get('website', None)
        image_link = body.get('image_link', None)
        facebook_link = body.get('facebook_link', None)
        seeking_venue = body.get('seeking_venue', False)
        seeking_description = body.get('seeking_description', None)

        if not name or not genres or not city or not state or \
            (phone and not is_valid_phone_number(phone)) or (website and not is_valid_url(website)) or \
                (image_link and not is_valid_url(image_link)) or (facebook_link and not is_valid_url(facebook_link)):
            abort(400)
        try:
            new_artist = Artist(name=name, genres=genres, city=city, state=state,
            phone=phone, website=website, image_link=image_link, facebook_link=facebook_link,
            seeking_venue=seeking_venue, seeking_description=seeking_description)
            new_artist.insert()
            artists = [artist.short() for artist in Artist.query.order_by(Artist.id).all()]
            return jsonify({
                'success': True,
                'artists': artists,
                'total_artists': len(artists)
            })

        except Exception as e:
            abort(422)

    '''
    Create a GET endpoint to get artists based on id
    '''
    @app.route('/api/artists/<int:artist_id>')
    def show_artist_api(artist_id):
        try:
            artist = Artist.query.filter(Artist.id == artist_id).one_or_none()
            if not artist:
                abort(404)

            return jsonify({
                'success': True,
                'artist': artist.long()
            })

        except Exception as e:
            abort(422)

    '''
    Create a PATCH endpoint to edit artists based on id
    '''
    @app.route('/api/artists/<int:artist_id>/edit', methods=['PATCH'])
    @requires_auth('patch:artists')
    def edit_artist_api(payload, artist_id):
        body = request.get_json()
        name = body.get('name', None)
        genres = body.get('genres', None)
        city = body.get('city', None)
        state = body.get('state', None)
        phone = body.get('phone', None)
        website = body.get('website', None)
        image_link = body.get('image_link', None)
        facebook_link = body.get('facebook_link', None)
        seeking_venue = body.get('seeking_venue', False)
        seeking_description = body.get('seeking_description', None)
        if not name or not genres or not city or not state or \
            (phone and not is_valid_phone_number(phone)) or (website and not is_valid_url(website)) or \
                (image_link and not is_valid_url(image_link)) or (facebook_link and not is_valid_url(facebook_link)):
            abort(400)

        try:
            artist = Artist.query.filter(Artist.id == artist_id).one_or_none()
            if not artist:
                abort(404)
            artist.name = name
            artist.city = city
            artist.state = state
            artist.genres = genres
            artist.phone = phone
            artist.website = website
            artist.image_link = image_link
            artist.facebook_link = facebook_link
            artist.seeking_venue = seeking_venue
            artist.seeking_description = seeking_description

            artist.update()
            return jsonify({
                'success': True,
                'artist': artist.long()
            })

        except Exception as e:
            abort(422)

    '''
    Create a PATCH endpoint to delete artists based on id
    '''
    @app.route('/api/artists/<artist_id>', methods=['DELETE'])
    @requires_auth('delete:artists')
    def delete_artist_api(payload, artist_id):
        try:
            artist = Artist.query.filter(Artist.id == artist_id).one_or_none()
            if not artist:
                abort(404)
            artist.delete()
            return jsonify({
                'success': True,
                'delete': artist.short()
            })

        except Exception as e:
            abort(422)

    #  Shows

    @app.route('/shows')
    def shows():
        # displays list of shows at /shows
        #       num_shows should be aggregated based on number of upcoming shows per venue.
        data = []
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
    # @requires_auth('post:shows')
    def create_shows():
        # renders form. do not touch.
        form = ShowForm()
        return render_template('forms/new_show.html', form=form)

    @app.route('/shows/create', methods=['POST'])
    # @requires_auth('post:shows')
    def create_show_submission():
        # called to create new shows in the db, upon submitting new show listing form
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

    #  Show APIs
    @app.route('/api/shows')
    def shows_api():
        try:
            shows = [show.format() for show in Show.query.order_by(Show.id).all()]
            return jsonify({
                'success': True,
                'shows': shows,
                'total_shows': len(shows)
            })

        except Exception as e:
            abort(422)

    @app.route('/api/shows/create', methods=['POST'])
    @requires_auth('post:shows')
    def create_shows_api(payload):
        body = request.get_json()

        start_time = body.get('start_time', None)
        venue_id = body.get('venue_id', None)
        artist_id = body.get('artist_id', None)

        if not start_time or not venue_id or not artist_id:
            abort(400)

        venue = Venue.query.filter(Venue.id == venue_id).one_or_none()
        artist = Artist.query.filter(Artist.id == artist_id).one_or_none()

        if not venue or not artist:
            abort(404)

        try:
            new_show = Show(start_time=start_time, venue_id=venue_id, artist_id=artist_id)
            new_show.insert()
            return jsonify({
                'success': True,
                'venue': venue.short(),
                'artist': artist.short(),
                'show': new_show.format()
            })

        except Exception as e:
            abort(422)

    '''
    implement error handler for 400
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    '''
    implement error handler for 401
    '''
    @app.errorhandler(401)
    def not_authorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Not authorized"
        }), 401

    '''
    implement error handler for 404
    '''
    @app.errorhandler(404)
    def notfound(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
            }), 404

    '''
    implement error handler for 422
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
            }), 422

    '''
    implement error handler for AuthError
        error handler should conform to general task above
    '''
    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    if not app.debug:
        file_handler = FileHandler('error.log')
        file_handler.setFormatter(
            Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        )
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('errors')

    return app

# Launch.


app = create_app()
if __name__ == '__main__':
    app.run()
