from datetime import date
from modapp import Venue


venu = """missing data in venu
        "past_shows": [{
            "artist_id": 4,
            "artist_name": "Guns N Petals",
            "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
            "start_time": "2019-05-21T21:30:00.000Z"
        }],
        "upcoming_shows": [],
        "past_shows_count": 1,
        "upcoming_shows_count": 0,"""

artist = """{missing data
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "past_shows": [{
            "venue_id": 1,
            "venue_name": "The Musical Hop",
            "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
            "start_time": "2019-05-21T21:30:00.000Z"
        }],
        "upcoming_shows": [],
        "past_shows_count": 1,
        "upcoming_shows_count": 0,
    }"""


"""
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), nullable=False)
    show_date = db.Column(db.DateTime, nullable=False,
                          default=datetime.datetime.utcnow)
"""
data1 = {
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!"}


veunu1 = Venue(name='The Musical Hop', genres=["Jazz", "Reggae", "Swing", "Classical", "Folk"], address='1015 Folsom Street', city='San Francisco', state='CA', phone='1231231234', website='https://www.themusicalhop.com', facebook_link='https: // www.facebook.com/TheMusicalHop',
               seeking_talent=True, seeking_description='We are on the lookout for a local artist to play every two weeks. Please call us.', image_link='https: // images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1 & ixid=eyJhcHBfaWQiOjEyMDd9 & auto=format & fit=crop & w=400 & q=60')


order_items = db.Table('order_items',
                       db.Column('order_id', db.Integer, db.ForeignKey(
                           'order.id'), primary_key=True),
                       db.Column('product_id', db.Integer, db.ForeignKey(
                           'product.id'), primary_key=True)
                       )


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(), nullable=False)
    products = db.relationship('Product', secondary=order_items,
                               backref=db.backref('orders', lazy=True))


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)


data = date
data1 = data1.append({
    "id": data.id,
    "name": data.name,
    "genres": data.genres,
    "address": data.address,
    "city": data.city,
    "state": data.state,
    "phone": data.phone,
    "website": data.website,
    "facebook_link": data.facebook_link,
    "seeking_talent": data.seeking_talent,
    "seeking_description": data.seeking_description
})
# id = db.Column(db.Integer, primary_key=True)
# artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
# venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
# start_time = db.Column(db.DateTime, nullable=False,
#                        default=datetime.now())


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
                           default='https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60')
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
                           default='https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80')
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


for i in range(len(result)):
    print(i)
    for a in result:
        print(a)
        data.append({
            "venue_id": a[i].d,
            "venue_name": Venue.name,
            "artist_id": Artist.id,
            "artist_name": Artist.name,
            "artist_image_link": Artist.image_link,
        })
        print(data)

result = None
# result = db.session.query(SELECT show.venue_id AS show_venue_id, "Venue".name AS "Venue_name", show.artist_id AS show_artist_id, "Artist".name AS "Artist_name", "Artist".image_link AS "Artist_image_link", show.start_time AS show_start_time
                          FROM show, "Venue", "Artist"
                          WHERE "Venue".id = show.venue_id AND "Artist".id = show.artist_id)


result=db.session.query(Show.venue_id, Venue.name, Show.artist_id,
                          Artist.name, Artist.image_link, Show.start_time)
result=result.filter(Venue.id == Show.venue_id, Artist.id == Show.artist_id)

result=db.session.query(Show.venue_id, Venue.name, Show.artist_id, Artist.name, Artist.image_link,
                          Show.start_time).filter(Venue.id == Show.venue_id, Artist.id == Show.artist_id)
