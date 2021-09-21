#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import dateutil.parser
from flask import Flask, render_template, request, Response, redirect, url_for, abort, flash
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys
from models import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
db = connect_db(app)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


# def format_datetime(value, format='medium'):
#     if isinstance(value, str):
#         date = dateutil.parser.parse(value)
#     else:
#         date = value


# app.jinja_env.filters['datetime'] = format_datetime


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

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    result = Venue.query.filter(Venue.name.ilike(
        '%' + request.form.get('search_term') + '%'))
    response = {}
    response['count'] = result.count()
    response['data'] = result
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    selected_venue = Venue.query.filter_by(
        id=venue_id).first()

    past_shows = db.session.query(Show).join(Artist).filter(
        Show.venue_id == venue_id).filter(Show.start_time < datetime.now()).all()
    upcoming_shows = db.session.query(Show).join(Artist).filter(
        Show.venue_id == venue_id).filter(Show.start_time > datetime.now()).all()
    past_data = []
    for s, a in db.session.query(Show, Artist).filter(Show.venue_id == venue_id).filter(Show.start_time < datetime.now()).all():
        past_data.append({
            'artist_id': a.id,
            'artist_name': a.name,
            'artist_image_link': a.image_link,
            'start_time': s.start_time
        })

    upcome_data = []
    for s, a in db.session.query(Show, Venue).filter(Show.venue_id == venue_id).filter(Show.start_time > datetime.now()).all():
        upcome_data.append({
            'artist_id': a.id,
            'artist_name': a.name,
            'artist_image_link': a.image_link,
            'start_time': s.start_time
        })

    selected_venue.past_shows_count = len(past_shows)
    selected_venue.past_shows = past_data
    selected_venue.upcoming_shows_count = len(upcoming_shows)
    selected_venue.upcoming_shows = upcome_data

    return render_template('pages/show_venue.html', venue=selected_venue)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
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
        form = VenueForm()
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
        # Update DB
        db.session.add(venue)
        db.session.commit()
        flash('Venue: {0} created successfully'.format(venue.name))
    except Exception as err:
        flash('An error occurred creating the Venue: {0}. Error: {1}'.format(
            venue.name, err))
        db.session.rollback()
    finally:
        db.session.close()
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
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


#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # shows all artist
    data = Artist.query.order_by('id').all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # shows the artist result with search terms
    result = Artist.query.filter(Artist.name.ilike(
        '%' + request.form.get('search_term') + '%'))

    response = {}
    response['count'] = result.count()
    response['data'] = result
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    selected_artist = Artist.query.filter_by(id=artist_id).order_by(
        'id').first()
    past_shows = db.session.query(Show).join(Venue).filter(
        Show.artist_id == artist_id).filter(Show.start_time < datetime.now()).all()
    upcoming_shows = db.session.query(Show).join(Venue).filter(
        Show.artist_id == artist_id).filter(Show.start_time > datetime.now()).all()
    past_data = []
    for s, v in db.session.query(Show, Venue).filter(Show.artist_id == artist_id).filter(Show.start_time < datetime.now()).all():
        past_data.append({
            'venue_id': v.id,
            'venue_name': v.name,
            'venue_image_link': v.image_link,
            'start_time': s.start_time
        })

    upcome_data = []
    for s, v in db.session.query(Show, Venue).filter(Show.artist_id == artist_id).filter(Show.start_time > datetime.now()).all():
        upcome_data.append({
            'venue_id': v.id,
            'venue_name': v.name,
            'venue_image_link': v.image_link,
            'start_time': s.start_time
        })

    selected_artist.past_shows_count = len(past_shows)
    selected_artist.past_shows = past_data
    selected_artist.upcoming_shows_count = len(upcoming_shows)
    selected_artist.upcoming_shows = upcome_data
    return render_template('pages/show_artist.html', artist=selected_artist)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.filter_by(id=artist_id).first()
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
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
        form = ArtistForm()
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
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
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
    if error:
        abort(500)
    if not error:
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
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
    # called to create new shows in the db, upon submitting new show listing form
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
