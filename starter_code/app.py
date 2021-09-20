#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
from datetime import datetime


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# TODO: connect to a local postgresql database  # done

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    # instead of just date = dateutil.parser.parse(value)
    if isinstance(value, str):
        date = dateutil.parser.parse(value)
    else:
        date = value


app.jinja_env.filters['datetime'] = format_datetime


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

    # TODO: implement any missing fields, as a database migration using Flask-Migrate   # done


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

    # TODO: implement any missing fields, as a database migration using Flask-Migrate   # done


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
# TODO Implement Show and Artist models, and complete all model relationships and properties, \
# as a database migration.  # done


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
    # TODO: replace with real venues data.                                              # done
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    result = Venue.query.group_by(Venue.city, Venue.state, Venue.id).all()
    data = []
    for venue in result:
        data.append({
            "city": venue.city,
            "state": venue.state,
            "venues": [{
                "id": venue.id,
                "name": venue.name}]
        })

    print(data)
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.  # done
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    result = Venue.query.filter(Venue.name.ilike(
        '%' + request.form.get('search_term') + '%'))
    # for debug
    # print(result)
    response = {}
    response['count'] = result.count()
    response['data'] = result
    response1 = {
        "count": 1,
        "data": [{
            "id": 2,
            "name": "The Dueling Pianos Bar",
            "num_upcoming_shows": 0,
        }]
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id          # done
    # TODO: replace with real venue data from the venues table, using venue_id
    selected_venue = Venue.query.filter_by(
        id=venue_id).first()  # check (the return of venue)

    return render_template('pages/show_venue.html', venue=selected_venue)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead               # done
    # TODO: modify data to be the data object returned from db insertion            # done
    print(request.form['name'])
    error = False
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    image_link = request.form['image_link']
    facebook_link = request.form['facebook_link']
    genres = request.form['genres']
    website = request.form['website_link']
    seeking_talent = True if 'seeking_talent' in request.form else False
    seeking_description = request.form['seeking_description']
    print(name, city)
    try:
        venue = Venue(
            name=name,
            city=city,
            state=state,
            address=address,
            phone=phone,
            image_link=image_link,
            facebook_link=facebook_link,
            genres=genres,
            website=website,
            seeking_talent=seeking_talent,
            seeking_description=seeking_description,
        )
        print(venue)
        # Update DB
        db.session.add(venue)
        db.session.commit()
    except Exception:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    # TODO: on unsuccessful db insert, flash an error instead.                  # done
    if error:
        abort(500)
    if not error:
        flash('Venue ' + request.form['name'] + ' was successfully listed!')

    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using                         # done
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.   # done

    error = False
    try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return redirect(url_for('index'))

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that        # if
    # clicking that button delete it from the db then redirect the user to the homepage             # if

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database          # done
    data = Artist.query.order_by('id').all()
    data1 = [{
        "id": 4,
        "name": "Guns N Petals",
    }, {
        "id": 5,
        "name": "Matt Quevedo",
    }, {
        "id": 6,
        "name": "The Wild Sax Band",
    }]
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.  # done
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    result = Artist.query.filter(Artist.name.ilike(
        '%' + request.form.get('search_term') + '%'))

    response = {}
    response['count'] = result.count()
    response['data'] = result

    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id                                    # done
    # TODO: replace with real artist data from the artist table, using artist_id
    selected_artist = Artist.query.filter_by(id=artist_id).order_by(
        'id').first()

    return render_template('pages/show_artist.html', artist=selected_artist)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    # TODO: populate form with fields from artist with ID <artist_id>               # done
    form = ArtistForm()
    artist = Artist.query.filter_by(id=artist_id).first()

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing        # done
    # artist record with ID <artist_id> using the new attributes
    error = False
    form = ArtistForm()
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    genres = request.form['genres']
    image_link = request.form['image_link']
    facebook_link = request.form['facebook_link']
    website = request.form['website_link']
    seeking_venue = True if 'seeking_talent' in request.form else False
    seeking_description = request.form['seeking_description']
    try:
        artist = Artist.query.get(artist_id)
        artist.name = name
        artist.city = city
        artist.state = state
        artist.phone = phone
        artist.genres = genres
        artist.image_link = image_link
        artist.facebook_link = facebook_link
        artist.website = website
        artist.seeking_venue = seeking_venue
        artist.seeking_description = seeking_description
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.filter_by(id=venue_id).first()
    # TODO: populate form with values from venue with ID <venue_id>     # done
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing            # done
    # venue record with ID <venue_id> using the new attributes
    error = False
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    genres = request.form['genres']
    image_link = request.form['image_link']
    facebook_link = request.form['facebook_link']
    website = request.form['website_link']
    seeking_talent = True if 'seeking_talent' in request.form else False
    seeking_description = request.form['seeking_description']

    try:
        venue = Venue.query.get(venue_id)
        venue.name = name
        venue.city = city
        venue.state = state
        venue.address = address
        venue.phone = phone
        venue.genres = genres
        venue.image_link = image_link
        venue.facebook_link = facebook_link
        venue.website = website
        venue.seeking_talent = seeking_talent
        venue.seeking_description = seeking_description
        db.session.commit()
    except Exception:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
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
    # TODO: insert form data as a new Venue record in the db, instead    # done
    # TODO: modify data to be the data object returned from db insertion
    error = False
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    genres = request.form['genres']
    image_link = request.form['image_link']
    facebook_link = request.form['facebook_link']
    website = request.form['website_link']
    seeking_venue = True if 'seeking_talent' in request.form else False
    seeking_description = request.form['seeking_description']

    try:
        artists = Artist(
            name=name,
            city=city,
            state=state,
            phone=phone,
            genres=genres,
            image_link=image_link,
            facebook_link=facebook_link,
            website=website,
            seeking_venue=seeking_venue,
            seeking_description=seeking_description,
        )

        db.session.add(artists)
        db.session.commit()
    except Exception:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    # TODO: on unsuccessful db insert, flash an error instead.                  # done
    if error:
        abort(500)
    if not error:
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # on successful db insert, flash success                                    # done
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows                      # done
    # TODO: replace with real venues data.
    # result = Show.query.order_by('id').all()

    #     result = db.session.execute(SELECT "Venue".name AS "Venue_name", "Artist".name AS "Artist_name", "Artist".image_link AS "Artist_image_link", show.venue_id AS show_venue_id, show.artist_id AS show_artist_id, show.start_time AS show_start_time, show.id AS show_id
    # FROM "Venue", "Artist", show;)

    result = db.session.query(Show.venue_id, Venue.name, Show.artist_id,
                              Artist.name, Artist.image_link, Show.start_time)
    result = result.filter(Venue.id == Show.venue_id,
                           Artist.id == Show.artist_id)
    data = []
    for i in result:
        data.append({
            'venue_id': i[0],
            'venue_name': i[1],
            'artist_id': i[2],
            'artist_name': i[3],
            'artist_image_link': i[4],
            'start_time': i[5]
        })

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form       #done
    # TODO: insert form data as a new Show record in the db, instead
    error = False
    artist_id = request.form['artist_id']
    venue_id = request.form['venue_id']
    start_time = request.form['start_time']

    try:
        show = Show(
            artist_id=artist_id,
            venue_id=venue_id,
            start_time=start_time,
        )

        # Update DB
        db.session.add(show)
        db.session.commit()
    except Exception:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    if not error:
        flash('Show was successfully listed!')

    # TODO: on unsuccessful db insert, flash an error instead.                  # done

    # on successful db insert, flash success

    # TODO: on unsuccessful db insert, flash an error instead.              # done
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
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
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
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
    app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
