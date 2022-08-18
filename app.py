#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from lib2to3.pgen2 import driver
from operator import itemgetter
import dateutil.parser
import babel
from flask import (
    Flask, 
    render_template, 
    request, 
    Response, 
    flash, 
    redirect, 
    url_for)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_migrate import Migrate
from flask_wtf import Form
from flask_wtf import FlaskForm
from sqlalchemy import false, true
from DateTime import DateTime
from datetime import datetime
from forms import *
import config
from models import Venue, Artist, Show 

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#


app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

db.init_app(app)




# moment = Moment(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Luckystar01@localhost:5432/fyyurapp"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False







# db.init_app(app) # Just initiate it here.



# TODO: connect to a local postgresql database


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

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
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  venues = Venue.query.all()

  places = Venue.query.distinct(Venue.city, Venue.state).all()

  for place in places:
        data.append({
            'city': place.city,
            'state': place.state,
            'venues': [{
                'id': venue.id,
                'name': venue.name,
                'num_upcoming_shows': len([show for show in venue.shows if show.start_time > datetime.now()])
            } for venue in venues if
                venue.city == place.city and venue.state == place.state]
        })
  return render_template('pages/venues.html', areas=data)
  

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  result = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')) 
  response = {
    'count': result.count(),
    'data': result
  }

  return render_template('pages/search_venues.html', results=response, search_term =search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  venue = Venue.query.get_or_404(venue_id)
  upcoming_shows_query = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time>datetime.now()).all()
  past_shows_query = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time<datetime.now()).all()
  
  past_shows = []
  upcoming_shows = []

  for show in upcoming_shows_query:
    upcoming_shows.append({
      'artist_id': show.artist_id,
      'artist_name': show.artist.name,
      'artist_image_link': show.artist.image_link,
      'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
    })

  
  for show in past_shows_query:
    past_shows.append({
      'artist_id': show.artist_id,
      'artist_name': show.artist.name,
      'artist_image_link': show.artist.image_link,
      'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
    })

  # object class to dict
  data = vars(venue)

  data['past_shows'] = past_shows
  data['upcoming_shows'] = upcoming_shows
  data['past_shows_count'] = len(past_shows)
  data['upcoming_shows_count'] = len(upcoming_shows)
 
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm(request.form)
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = VenueForm(request.form, meta={'csrf': False})
  if form.validate():
      try:
      # get form data and create
        venue = Venue()
        # form.populate_obj(venue)
        
        
        venue = Venue(name=form.name.data, city=form.city.data, state=form.state.data, address=form.address.data,
                      phone=form.phone.data, image_link=form.image_link.data, genres=form.genres.data,
                      facebook_link=form.facebook_link.data, seeking_description=form.seeking_description.data,
                      website=form.website_link.data, seeking_talent=form.seeking_talent.data)
        
        db.session.add(venue)
        db.session.commit()

      # on successful db insert, flash success

        flash('Venue ' + request.form['name'] + ' was successfully listed!')
      
      
      
      # TODO: on unsuccessful db insert, flash an error instead.
      except:
        db.session.rollback()
        flash('An error occurred. Venue'+ request.form['name'] + ' could not be listed')
      
      finally:
      # session close
        db.session.close()
  else:
    message = []
    for field, err in form.errors.items():
        message.append(field + ' ' + '|'.join(err))
    flash('Errors ' + str(message))

# e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
# see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>/', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    # get Venue by id
    venue = Venue.query.get(venue_id)
    venue_name = venue.name

    db.session.delete(venue)
    db.session.commit()

    flash('Venue ' + venue_name + ' was deleted')
  except:
    flash(' an error occured and Venue ' + venue_name + ' was not deleted')
    db.session.rollback()
  finally:
    db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('index'))



#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = []
  
  artists = Artist.query.all()
  for artist in artists:
    data.append({
      "id": artist.id,
      "name": artist.name
    })


  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')

  # case-insensitive search
  result = Artist.query.filter(Artist.name.ilike(f'%{search_term}%'))

  response = {
    'count': result.count(),
    'data': result
  }

  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id

  artist = Artist.query.get_or_404(artist_id)

  upcoming_shows_query = db.session.query(Show).join(Artist).filter(Show.artist_id==artist_id).filter(Show.start_time>datetime.now()).all()
  past_shows_query = db.session.query(Show).join(Artist).filter(Show.artist_id==artist_id).filter(Show.start_time<datetime.now()).all()
  
  past_shows = []
  upcoming_shows = []

  for show in upcoming_shows_query:
    upcoming_shows.append({
      'artist_id': show.artist_id,
      'artist_name': show.artist.name,
      'venue_image_link': show.venue.image_link,
      'artist_image_link': show.artist.image_link,
      'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
    })

  
  for show in past_shows_query:
    past_shows.append({
      'artist_id': show.artist_id,
      'artist_name': show.artist.name,
      'venue_image_link': show.venue.image_link,
      'artist_image_link': show.artist.image_link,
      'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
    })

  # # object class to dict
  data = vars(artist)
  
  data['past_shows'] = past_shows
  data['upcoming_shows'] = upcoming_shows
  data['past_shows_count'] = len(past_shows)
  data['upcoming_shows_count'] = len(upcoming_shows)
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm(request.form)
  artist = Artist.query.get(artist_id)

  artist_data={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "facebook_link": artist.facebook_link,
    "image_link": artist.image_link
  }

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  try:
    form = ArtistForm(request.form)
    artist = Artist.query.get(artist_id)
    
    name = form.name.data

    artist.name = name
    artist.phone = form.phone.data
    artist.state = form.state.data
    artist.city = form.city.data
    artist.genres = form.genres.data
    artist.image_link = form.image_link.data
    artist.facebook_link = form.facebook_link.data

    db.session.commit()
    flash('The Artist ' + request.form['name'] + ' has been successfully updated!')
  except:
    db.session.rollback()
    flash('An Error has occured and the update unsucessful')
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm(request.form)
  venue = Venue.query.get(venue_id)
  venue = {
    "id": venue_id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website":venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link
  }  

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  try:
    form = VenueForm(request.form)
    venue = Venue.query.get(venue_id)
    name = VenueForm.name.data

    venue.name = name
    venue.genres = form.genres.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.address = form.address.data
    venue.phone = form.phone.data
    venue.facebook_link = form.facebook_link.data
    venue.website = form.website_link.data
    venue.image_link = form.image_link.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data

    db.session.commit()
    flash('Venue ' + name + 'has been updated')
  except:
    db.session.rollback()
    flash('An error occured while trying to update Venue')
  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm(request.form)
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm(request.form, meta={'csrf': False})
  if form.validate():
    try:

      artist = Artist()
      artist = Artist(name=form.name.data,
                      city=form.city.data, 
                      state=form.state.data,
                      phone=form.phone.data, 
                      genres=form.genres.data,
                      image_link=form.image_link.data, 
                      facebook_link=form.facebook_link.data,
                      seeking_venue = True if form.seeking_venue.data=='Yes' else False,
                      seeking_description = form.seeking_description.data.strip(),
                      website = form.website_link.data
                    )
      db.session.add(artist)
      db.session.commit()
    # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    except:
      db.session.rollback()
      flash('An error ocurred, Artist ' + request.form['name'] + ' could not be listed')
    finally:
      db.session.close()
  else:
    message = []
    for field, err in form.errors.items():
        message.append(field + ' ' + '|'.join(err))
    flash('Errors ' + str(message))
  return render_template('pages/home.html') 


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  # shows = Show.query.all()

  shows = db.session.query(Show).join(Venue).all()

  data = []
  for show in shows:
    data.append({
      'venue_id': show.venue_id,
      'venue_name': show.venue.name,
      'artist_id': show.artist_id,
      'artist_name': show.artist.name,
      'artist_image_link': show.artist.image_link,
      'start_time': format_datetime(str(show.start_time))
    })
    

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm(request.form)
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm(request.form, meta={'csrf': False})
  if form.validate():
    try:
      show = Show()
      show = Show(artist_id=form.artist_id.data, 
                  venue_id=form.venue_id.data,
                  start_time=form.start_time.data)
      db.session.add(show)
      db.session.commit()
    # on successful db insert, flash success
      flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    except:
      db.session.rollback()
      flash('An error occured. show could not be listed')
    finally:
      db.session.close()
  else:
    message = []
    for field, err in form.errors.items():
        message.append(field + ' ' + '|'.join(err))
    flash('Errors ' + str(message))
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
